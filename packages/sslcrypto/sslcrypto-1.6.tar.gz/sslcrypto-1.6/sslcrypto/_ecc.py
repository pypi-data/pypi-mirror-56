import hashlib
import hmac
import base58check


try:
    hashlib.new("ripemd160")
except ValueError:
    # No native implementation
    from . import _ripemd
    def ripemd160(*args):
        return _ripemd.new(*args)
else:
    # Use OpenSSL
    def ripemd160(*args):
        return hashlib.new("ripemd160", *args)


class ECC:
    CURVES = (
        "secp112r1", "secp112r2",
        "secp128r1", "secp128r2",
        "secp160k1", "secp160r1", "secp160r2",
        "secp192k1", "prime192v1",
        "secp224k1", "secp224r1",
        "secp256k1", "prime256v1",
        "secp384r1",
        "secp521r1"
    )

    def __init__(self, backend, aes):
        self._backend = backend
        self._aes = aes


    def get_curve(self, name):
        if name not in self.CURVES or not self._backend.is_supported(name):
            raise ValueError("Unknown curve {}".format(name))
        return EllipticCurve(self._backend, self._aes, name)


class EllipticCurve:
    def __init__(self, backend, aes, name):
        self._backend = backend.EllipticCurveBackend(name)
        self._aes = aes
        self.name = name


    def _encode_public_key(self, x, y):
        return bytes([0x02 + (y[-1] % 2)]) + x


    def _decode_public_key(self, public_key, partial=False):
        if not public_key:
            raise ValueError("No public key")

        if public_key[0] == 0x04:
            # Uncompressed
            expected_length = 1 + 2 * self._backend.public_key_length
            if partial:
                if len(public_key) < expected_length:
                    raise ValueError("Invalid uncompressed public key length")
            else:
                if len(public_key) != expected_length:
                    raise ValueError("Invalid uncompressed public key length")
            x = public_key[1:1 + self._backend.public_key_length]
            y = public_key[1 + self._backend.public_key_length:expected_length]
            if partial:
                return (x, y), expected_length
            else:
                return x, y
        elif public_key[0] in (0x02, 0x03):
            # Compressed
            expected_length = 1 + self._backend.public_key_length
            if partial:
                if len(public_key) < expected_length:
                    raise ValueError("Invalid compressed public key length")
            else:
                if len(public_key) != expected_length:
                    raise ValueError("Invalid compressed public key length")

            x, y = self._backend.decompress_point(public_key[:expected_length])
            # Sanity check
            if x != public_key[1:expected_length]:
                raise ValueError("Incorrect compressed public key")
            if partial:
                return (x, y), expected_length
            else:
                return x, y
        else:
            raise ValueError("Invalid public key prefix")


    def new_private_key(self):
        return self._backend.new_private_key()


    def private_to_public(self, private_key):
        x, y = self._backend.private_to_public(private_key)
        return self._encode_public_key(x, y)


    def private_to_wif(self, private_key):
        h = hashlib.sha256(b"\x80" + private_key).digest()
        h = hashlib.sha256(h).digest()
        checksum = h[:4]
        return base58check.b58encode(b"\x80" + private_key + checksum)


    def wif_to_private(self, wif):
        dec = base58check.b58decode(wif)
        if dec[0] != 0x80:
            raise ValueError("Invalid network (expected mainnet)")
        private_key = dec[1:-4]
        checksum = dec[-4:]
        # Compare checksum
        h = hashlib.sha256(b"\x80" + private_key).digest()
        h = hashlib.sha256(h).digest()
        if h[:4] != checksum:
            raise ValueError("Invalid checksum")
        return private_key


    def public_to_address(self, public_key):
        # Decompress public key
        public_key = b"\x04" + b"".join(self._decode_public_key(public_key))
        # Calculate hash160
        h = hashlib.sha256(public_key).digest()
        hash160 = ripemd160(h).digest()
        # Add checksum
        h = hashlib.sha256(b"\x00" + hash160).digest()
        h = hashlib.sha256(h).digest()
        checksum = h[:4]
        return base58check.b58encode(b"\x00" + hash160 + checksum)


    def private_to_address(self, private_key):
        # Kinda useless but left for quick migration from pybitcointools
        return self.public_to_address(self.private_to_public(private_key))


    def derive(self, private_key, public_key):
        if not isinstance(public_key, tuple):
            public_key = self._decode_public_key(public_key)
        return self._backend.ecdh(private_key, public_key)


    def _digest(self, data, hash):
        if hash is None:
            return data
        elif callable(hash):
            return hash(data)
        elif hash == "sha1":
            return hashlib.sha1(data).digest()
        elif hash == "sha256":
            return hashlib.sha256(data).digest()
        elif hash == "sha512":
            return hashlib.sha512(data).digest()
        else:
            raise ValueError("Unknown hash/derivation method")


    # High-level functions
    def encrypt(self, data, public_key, algo="aes-256-cbc", derivation="sha256", mac="hmac-sha256", return_aes_key=False):
        # Generate ephemeral private key
        private_key = self.new_private_key()

        # Derive key
        ecdh = self.derive(private_key, public_key)
        key = self._digest(ecdh, derivation)
        k_enc_len = self._aes.get_algo_key_length(algo)
        if len(key) < k_enc_len:
            raise ValueError("Too short digest")
        k_enc, k_mac = key[:k_enc_len], key[k_enc_len:]

        # Encrypt
        ciphertext, iv = self._aes.encrypt(data, k_enc, algo=algo)
        ciphertext = iv + self.private_to_public(private_key) + ciphertext

        # Add MAC tag
        if callable(mac):
            tag = mac(k_mac, ciphertext)
        elif mac == "hmac-sha256":
            h = hmac.new(k_mac, digestmod="sha256")
            h.update(ciphertext)
            tag = h.digest()
        elif mac == "hmac-sha512":
            h = hmac.new(k_mac, digestmod="sha512")
            h.update(ciphertext)
            tag = h.digest()
        elif mac is None:
            tag = b""
        else:
            raise ValueError("Unsupported MAC")

        if return_aes_key:
            return ciphertext + tag, k_enc
        else:
            return ciphertext + tag


    def decrypt(self, ciphertext, private_key, algo="aes-256-cbc", derivation="sha256", mac="hmac-sha256"):
        # Get MAC tag
        if callable(mac):
            tag_length = mac.digest_size
        elif mac == "hmac-sha256":
            tag_length = hmac.new(b"", digestmod="sha256").digest_size
        elif mac == "hmac-sha512":
            tag_length = hmac.new(b"", digestmod="sha512").digest_size
        elif mac is None:
            tag_length = 0
        else:
            raise ValueError("Unsupported MAC")

        if len(ciphertext) < tag_length:
            raise ValueError("Ciphertext is too small to contain MAC tag")
        if tag_length == 0:
            tag = b""
        else:
            ciphertext, tag = ciphertext[:-tag_length], ciphertext[-tag_length:]

        orig_ciphertext = ciphertext

        if len(ciphertext) < 16:
            raise ValueError("Ciphertext is too small to contain IV")
        iv, ciphertext = ciphertext[:16], ciphertext[16:]

        public_key, pos = self._decode_public_key(ciphertext, partial=True)
        ciphertext = ciphertext[pos:]

        # Derive key
        ecdh = self.derive(private_key, public_key)
        key = self._digest(ecdh, derivation)
        k_enc_len = self._aes.get_algo_key_length(algo)
        if len(key) < k_enc_len:
            raise ValueError("Too short digest")
        k_enc, k_mac = key[:k_enc_len], key[k_enc_len:]

        # Verify MAC tag
        if callable(mac):
            expected_tag = mac(k_mac, orig_ciphertext)
        elif mac == "hmac-sha256":
            h = hmac.new(k_mac, digestmod="sha256")
            h.update(orig_ciphertext)
            expected_tag = h.digest()
        elif mac == "hmac-sha512":
            h = hmac.new(k_mac, digestmod="sha512")
            h.update(orig_ciphertext)
            expected_tag = h.digest()
        elif mac is None:
            expected_tag = b""

        if not hmac.compare_digest(tag, expected_tag):
            raise ValueError("Invalid MAC tag")

        return self._aes.decrypt(ciphertext, iv, k_enc, algo=algo)


    def sign(self, data, private_key, hash="sha256", recoverable=False, entropy=None):
        return self._backend.sign(self._digest(data, hash), private_key, recoverable, entropy)


    def recover(self, signature, data, hash="sha256"):
        # Sanity check: is this signature recoverable?
        if len(signature) != 1 + 2 * self._backend.public_key_length:
            raise ValueError("Cannot recover an unrecoverable signature")
        x, y = self._backend.recover(signature, self._digest(data, hash))
        return self._encode_public_key(x, y)


    def verify(self, signature, data, public_key, hash="sha256"):
        if len(signature) == 1 + 2 * self._backend.public_key_length:
            # Recoverable signature
            signature = signature[1:]
        if len(signature) != 2 * self._backend.public_key_length:
            raise ValueError("Invalid signature format")
        if not isinstance(public_key, tuple):
            public_key = self._decode_public_key(public_key)
        return self._backend.verify(signature, self._digest(data, hash), public_key)


    def derive_child(self, seed, child):
        # Based on BIP32
        if not 0 <= child < 2 ** 31:
            raise ValueError("Invalid child index")
        return self._backend.derive_child(seed, child)
