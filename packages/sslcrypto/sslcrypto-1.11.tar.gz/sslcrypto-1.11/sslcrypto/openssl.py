import ctypes
import os
import hmac
from ._ecc import ECC
from . import library


lib = library.discover_library()

# Initialize internal state
try:
    lib.OPENSSL_add_all_algorithms_conf()
except AttributeError:
    pass

# Initialize functions
try:
    lib.EVP_CIPHER_CTX_new.restype = ctypes.POINTER(ctypes.c_char)
except AttributeError:
    pass
lib.EVP_get_cipherbyname.restype = ctypes.POINTER(ctypes.c_char)
lib.BN_new.restype = ctypes.POINTER(ctypes.c_char)
lib.BN_bin2bn.restype = ctypes.POINTER(ctypes.c_char)
lib.BN_CTX_new.restype = ctypes.POINTER(ctypes.c_char)
lib.EC_GROUP_new_by_curve_name.restype = ctypes.POINTER(ctypes.c_char)
lib.EC_KEY_new_by_curve_name.restype = ctypes.POINTER(ctypes.c_char)
lib.EC_POINT_new.restype = ctypes.POINTER(ctypes.c_char)
lib.EC_KEY_get0_private_key.restype = ctypes.POINTER(ctypes.c_char)
lib.EVP_PKEY_new.restype = ctypes.POINTER(ctypes.c_char)
try:
    lib.EVP_PKEY_CTX_new.restype = ctypes.POINTER(ctypes.c_char)
except AttributeError:
    pass


class AES:
    ALGOS = (
        "aes-128-cbc", "aes-192-cbc", "aes-256-cbc",
        "aes-128-ctr", "aes-192-ctr", "aes-256-ctr",
        "aes-128-cfb", "aes-192-cfb", "aes-256-cfb",
        "aes-128-ofb", "aes-192-ofb", "aes-256-ofb"
    )

    def __init__(self):
        self.lib = lib  # For finalizer

        self.is_supported_ctx_new = hasattr(lib, "EVP_CIPHER_CTX_new")
        self.is_supported_ctx_reset = hasattr(lib, "EVP_CIPHER_CTX_reset")

        if self.is_supported_ctx_new:
            self.ctx = lib.EVP_CIPHER_CTX_new()
        else:
            # 1 KiB ought to be enough for everybody. We don't know the real
            # size of the context buffer because we are unsure about padding and
            # pointer size
            self.ctx = ctypes.create_string_buffer(1024)


    def __del__(self):
        if self.is_supported_ctx_new:
            self.lib.EVP_CIPHER_CTX_free(self.ctx)


    def _get_cipher(self, algo):
        if algo not in self.ALGOS:
            raise ValueError("Unknown cipher algorithm {}".format(algo))
        cipher = lib.EVP_get_cipherbyname(algo.encode())
        if not cipher:
            raise ValueError("Unknown cipher algorithm {}".format(algo))
        return cipher


    def get_algo_key_length(self, algo):
        # Initialize context
        if not self.is_supported_ctx_new:
            lib.EVP_CIPHER_CTX_init(self.ctx)
        try:
            # Get key length
            lib.EVP_EncryptInit_ex(self.ctx, self._get_cipher(algo), None, None, None)
            return lib.EVP_CIPHER_CTX_key_length(self.ctx)
        finally:
            if self.is_supported_ctx_reset:
                lib.EVP_CIPHER_CTX_reset(self.ctx)
            else:
                lib.EVP_CIPHER_CTX_cleanup(self.ctx)


    def new_key(self, algo="aes-256-cbc"):
        key_length = self.get_algo_key_length(algo)
        key = ctypes.create_string_buffer(key_length)
        lib.RAND_bytes(key, key_length)
        return bytes(key)


    def encrypt(self, data, key, algo="aes-256-cbc"):
        # Initialize context
        if not self.is_supported_ctx_new:
            lib.EVP_CIPHER_CTX_init(self.ctx)
        try:
            lib.EVP_EncryptInit_ex(self.ctx, self._get_cipher(algo), None, None, None)

            # Make sure key length is correct
            key_length = lib.EVP_CIPHER_CTX_key_length(self.ctx)
            if len(key) != key_length:
                raise ValueError("Expected key to be {} bytes, got {} bytes".format(key_length, len(key)))

            # Generate random IV
            iv_length = lib.EVP_CIPHER_CTX_iv_length(self.ctx)
            iv = os.urandom(iv_length)

            # Set key and IV
            lib.EVP_EncryptInit_ex(self.ctx, None, None, key, iv)

            # Actually encrypt
            block_size = lib.EVP_CIPHER_CTX_block_size(self.ctx)
            output = ctypes.create_string_buffer((len(data) // block_size + 1) * block_size)
            output_len = ctypes.c_int()

            if not lib.EVP_CipherUpdate(self.ctx, output, ctypes.byref(output_len), data, len(data)):
                raise ValueError("Could not feed cipher with data")

            new_output = ctypes.byref(output, output_len.value)
            output_len2 = ctypes.c_int()
            if not lib.EVP_CipherFinal_ex(self.ctx, new_output, ctypes.byref(output_len2)):
                raise ValueError("Could not finalize cipher")

            ciphertext = output[:output_len.value + output_len2.value]
            return ciphertext, iv
        finally:
            if self.is_supported_ctx_reset:
                lib.EVP_CIPHER_CTX_reset(self.ctx)
            else:
                lib.EVP_CIPHER_CTX_cleanup(self.ctx)


    def decrypt(self, ciphertext, iv, key, algo="aes-256-cbc"):
        # Initialize context
        if not self.is_supported_ctx_new:
            lib.EVP_CIPHER_CTX_init(self.ctx)
        try:
            lib.EVP_DecryptInit_ex(self.ctx, self._get_cipher(algo), None, None, None)

            # Make sure key length is correct
            key_length = lib.EVP_CIPHER_CTX_key_length(self.ctx)
            if len(key) != key_length:
                raise ValueError("Expected key to be {} bytes, got {} bytes".format(key_length, len(key)))

            # Make sure IV length is correct
            iv_length = lib.EVP_CIPHER_CTX_iv_length(self.ctx)
            if len(iv) != iv_length:
                raise ValueError("Expected IV to be {} bytes, got {} bytes".format(iv_length, len(iv)))

            # Make sure ciphertext length is correct
            block_size = lib.EVP_CIPHER_CTX_block_size(self.ctx)
            if len(ciphertext) % block_size != 0:
                raise ValueError(
                    "Expected ciphertext to be a multiple of {} bytes, got {} bytes".format(
                        block_size,
                        len(ciphertext)
                    )
                )

            # Set key and IV
            lib.EVP_DecryptInit_ex(self.ctx, None, None, key, iv)

            # Actually decrypt
            output = ctypes.create_string_buffer(len(ciphertext))
            output_len = ctypes.c_int()

            if not lib.EVP_DecryptUpdate(self.ctx, output, ctypes.byref(output_len), ciphertext, len(ciphertext)):
                raise ValueError("Could not feed decipher with ciphertext")

            new_output = ctypes.byref(output, output_len.value)
            output_len2 = ctypes.c_int()
            if not lib.EVP_DecryptFinal_ex(self.ctx, new_output, ctypes.byref(output_len2)):
                raise ValueError("Could not finalize decipher")

            return output[:output_len.value + output_len2.value]
        finally:
            if self.is_supported_ctx_reset:
                lib.EVP_CIPHER_CTX_reset(self.ctx)
            else:
                lib.EVP_CIPHER_CTX_cleanup(self.ctx)



class BN:
    def __init__(self, value=None, link_only=False):
        if link_only:
            self.bn = value
            self._free = False
        else:
            if value is None:
                self.bn = lib.BN_new()
                self._free = True
            elif isinstance(value, bytes):
                self.bn = lib.BN_bin2bn(value, len(value), None)
                self._free = True
            else:
                self.bn = lib.BN_new()
                lib.BN_clear(self.bn)
                lib.BN_add_word(self.bn, value)
                self._free = True


    def __del__(self):
        if self._free:
            lib.BN_free(self.bn)


    def bytes(self, length=None):
        buf = ctypes.create_string_buffer((len(self) + 7) // 8)
        lib.BN_bn2bin(self.bn, buf)
        buf = bytes(buf)
        if length is None:
            return buf
        else:
            if length < len(buf):
                raise ValueError("Too little space for BN")
            return b"\x00" * (length - len(buf)) + buf

    def __int__(self):
        value = 0
        for byte in self.bytes():
            value = value * 256 + byte
        return value

    def __len__(self):
        return lib.BN_num_bits(self.bn)


    def inverse(self, modulo):
        ctx = lib.BN_CTX_new()
        try:
            result = BN()
            if not lib.BN_mod_inverse(result.bn, self.bn, modulo.bn, ctx):
                raise ValueError("Could not compute inverse")
            return result
        finally:
            lib.BN_CTX_free(ctx)


    def __floordiv__(self, other):
        if not isinstance(other, BN):
            raise TypeError("Can only divide BN by BN, not {}".format(other))
        ctx = lib.BN_CTX_new()
        try:
            result = BN()
            if not lib.BN_div(result.bn, None, self.bn, other.bn, ctx):
                raise ZeroDivisionError("Division by zero")
            return result
        finally:
            lib.BN_CTX_free(ctx)

    def __mod__(self, other):
        if not isinstance(other, BN):
            raise TypeError("Can only divide BN by BN, not {}".format(other))
        ctx = lib.BN_CTX_new()
        try:
            result = BN()
            if not lib.BN_div(None, result.bn, self.bn, other.bn, ctx):
                raise ZeroDivisionError("Division by zero")
            return result
        finally:
            lib.BN_CTX_free(ctx)

    def __add__(self, other):
        if not isinstance(other, BN):
            raise TypeError("Can only sum BN's, not BN and {}".format(other))
        result = BN()
        if not lib.BN_add(result.bn, self.bn, other.bn, None):
            raise ValueError("Could not sum two BN's")
        return result

    def __sub__(self, other):
        if not isinstance(other, BN):
            raise TypeError("Can only subtract BN's, not BN and {}".format(other))
        result = BN()
        if not lib.BN_sub(result.bn, self.bn, other.bn, None):
            raise ValueError("Could not subtract BN from BN")
        return result

    def __mul__(self, other):
        if not isinstance(other, BN):
            raise TypeError("Can only multiply BN by BN, not {}".format(other))
        ctx = lib.BN_CTX_new()
        try:
            result = BN()
            if not lib.BN_mul(result.bn, self.bn, other.bn, ctx):
                raise ValueError("Could not multiply two BN's")
            return result
        finally:
            lib.BN_CTX_free(ctx)

    def __neg__(self):
        return BN(0) - self


    # A dirty but nice way to update current BN and free old BN at the same time
    def __imod__(self, other):
        res = self % other
        self.bn, res.bn = res.bn, self.bn
        return self
    def __iadd__(self, other):
        res = self + other
        self.bn, res.bn = res.bn, self.bn
        return self
    def __isub__(self, other):
        res = self - other
        self.bn, res.bn = res.bn, self.bn
        return self
    def __imul__(self, other):
        res = self * other
        self.bn, res.bn = res.bn, self.bn
        return self


    def cmp(self, other):
        if not isinstance(other, BN):
            raise TypeError("Can only compare BN with BN, not {}".format(other))
        return lib.BN_cmp(self.bn, other.bn)

    def __eq__(self, other):
        return self.cmp(other) == 0
    def __lt__(self, other):
        return self.cmp(other) < 0
    def __gt__(self, other):
        return self.cmp(other) > 0
    def __ne__(self, other):
        return self.cmp(other) != 0
    def __le__(self, other):
        return self.cmp(other) <= 0
    def __ge__(self, other):
        return self.cmp(other) >= 0


    def __repr__(self):
        return "<BN {}>".format(int(self))

    def __str__(self):
        return str(int(self))


class ECCBackend:
    NIDS = {
        "secp112r1": 704,
        "secp112r2": 705,
        "secp128r1": 706,
        "secp128r2": 707,
        "secp160k1": 708,
        "secp160r1": 709,
        "secp160r2": 710,
        "secp192k1": 711,
        "prime192v1": 409,
        "secp224k1": 712,
        "secp224r1": 713,
        "secp256k1": 714,
        "prime256v1": 415,
        "secp384r1": 715,
        "secp521r1": 716
    }


    def is_supported(self, name):
        return name in self.NIDS


    class EllipticCurveBackend:
        def __init__(self, name):
            self.lib = lib  # For finalizer
            self.nid = ECCBackend.NIDS[name]
            self.group = lib.EC_GROUP_new_by_curve_name(self.nid)
            if not self.group:
                raise ValueError("Curve {} is unsupported by OpenSSL".format(name))

            self.order = BN()
            self.p = BN()
            lib.EC_GROUP_get_order(self.group, self.order.bn, None)
            lib.EC_GROUP_get_curve_GFp(self.group, self.p.bn, None, None, None)

            self.public_key_length = (len(self.p) + 7) // 8

            self.is_supported_evp_pkey_ctx = hasattr(lib, "EVP_PKEY_CTX_new")


        def __del__(self):
            self.lib.EC_GROUP_free(self.group)


        def _private_key_to_ec_key(self, private_key):
            eckey = lib.EC_KEY_new_by_curve_name(self.nid)
            if not eckey:
                raise ValueError("Failed to allocate EC_KEY")
            private_key = BN(private_key)
            if not lib.EC_KEY_set_private_key(eckey, private_key.bn):
                lib.EC_KEY_free(eckey)
                raise ValueError("Invalid private key")
            return eckey, private_key


        def _public_key_to_point(self, public_key):
            x = BN(public_key[0])
            y = BN(public_key[1])
            # EC_KEY_set_public_key_affine_coordinates is not supported by
            # OpenSSL 1.0.0 so we can't use it
            point = lib.EC_POINT_new(self.group)
            if not lib.EC_POINT_set_affine_coordinates_GFp(self.group, point, x.bn, y.bn, None):
                raise ValueError("Could not set public key affine coordinates")
            return point


        def _public_key_to_ec_key(self, public_key):
            eckey = lib.EC_KEY_new_by_curve_name(self.nid)
            if not eckey:
                raise ValueError("Failed to allocate EC_KEY")
            try:
                # EC_KEY_set_public_key_affine_coordinates is not supported by
                # OpenSSL 1.0.0 so we can't use it
                point = self._public_key_to_point(public_key)
                if not lib.EC_KEY_set_public_key(eckey, point):
                    raise ValueError("Could not set point")
                lib.EC_POINT_free(point)
                return eckey
            except Exception as e:
                lib.EC_KEY_free(eckey)
                raise e from None


        def _point_to_affine(self, point):
            # Convert to affine coordinates
            x = BN()
            y = BN()
            if lib.EC_POINT_get_affine_coordinates_GFp(self.group, point, x.bn, y.bn, None) != 1:
                raise ValueError("Failed to convert public key to affine coordinates")
            # Convert to binary
            if (len(x) + 7) // 8 > self.public_key_length:
                raise ValueError("Public key X coordinate is too large")
            if (len(y) + 7) // 8 > self.public_key_length:
                raise ValueError("Public key Y coordinate is too large")
            return x.bytes(self.public_key_length), y.bytes(self.public_key_length)


        def decompress_point(self, public_key):
            point = lib.EC_POINT_new(self.group)
            if not point:
                raise ValueError("Could not create point")
            try:
                if not lib.EC_POINT_oct2point(self.group, point, public_key, len(public_key), None):
                    raise ValueError("Invalid compressed public key")
                return self._point_to_affine(point)
            finally:
                lib.EC_POINT_free(point)


        def new_private_key(self):
            # Create random key
            eckey = lib.EC_KEY_new_by_curve_name(self.nid)
            lib.EC_KEY_generate_key(eckey)
            # To big integer
            private_key = BN(lib.EC_KEY_get0_private_key(eckey), link_only=True)
            # To binary
            private_key_buf = private_key.bytes()
            # Cleanup
            lib.EC_KEY_free(eckey)
            return private_key_buf


        def private_to_public(self, private_key):
            eckey, private_key = self._private_key_to_ec_key(private_key)
            try:
                # Derive public key
                point = lib.EC_POINT_new(self.group)
                try:
                    if not lib.EC_POINT_mul(self.group, point, private_key.bn, None, None, None):
                        raise ValueError("Failed to derive public key")
                    return self._point_to_affine(point)
                finally:
                    lib.EC_POINT_free(point)
            finally:
                lib.EC_KEY_free(eckey)


        def ecdh(self, private_key, public_key):
            if not self.is_supported_evp_pkey_ctx:
                # Use ECDH_compute_key instead
                # Create EC_KEY from private key
                eckey, _ = self._private_key_to_ec_key(private_key)
                try:
                    # Create EC_POINT from public key
                    point = self._public_key_to_point(public_key)
                    try:
                        key = ctypes.create_string_buffer(self.public_key_length)
                        if lib.ECDH_compute_key(key, self.public_key_length, point, eckey, None) == -1:
                            raise ValueError("Could not compute shared secret")
                        return bytes(key)
                    finally:
                        lib.EC_POINT_free(point)
                finally:
                    lib.EC_KEY_free(eckey)

            # Private key:
            # Create EC_KEY
            eckey, _ = self._private_key_to_ec_key(private_key)
            try:
                # Convert to EVP_PKEY
                pkey = lib.EVP_PKEY_new()
                if not pkey:
                    raise ValueError("Could not create private key object")
                try:
                    lib.EVP_PKEY_set1_EC_KEY(pkey, eckey)

                    # Public key:
                    # Create EC_KEY
                    peer_eckey = self._public_key_to_ec_key(public_key)
                    try:
                        # Convert to EVP_PKEY
                        peer_pkey = lib.EVP_PKEY_new()
                        if not peer_pkey:
                            raise ValueError("Could not create public key object")
                        try:
                            lib.EVP_PKEY_set1_EC_KEY(peer_pkey, peer_eckey)

                            # Create context
                            ctx = lib.EVP_PKEY_CTX_new(pkey, None)
                            if not ctx:
                                raise ValueError("Could not create EVP context")
                            try:
                                if lib.EVP_PKEY_derive_init(ctx) != 1:
                                    raise ValueError("Could not initialize key derivation")
                                if not lib.EVP_PKEY_derive_set_peer(ctx, peer_pkey):
                                    raise ValueError("Could not set peer")

                                # Actually derive
                                key_len = ctypes.c_int(0)
                                lib.EVP_PKEY_derive(ctx, None, ctypes.byref(key_len))
                                key = ctypes.create_string_buffer(key_len.value)
                                lib.EVP_PKEY_derive(ctx, key, ctypes.byref(key_len))

                                return bytes(key)
                            finally:
                                lib.EVP_PKEY_CTX_free(ctx)
                        finally:
                            lib.EVP_PKEY_free(peer_pkey)
                    finally:
                        lib.EC_KEY_free(peer_eckey)
                finally:
                    lib.EVP_PKEY_free(pkey)
            finally:
                lib.EC_KEY_free(eckey)


        def _subject_to_bn(self, subject):
            return BN(subject[:(len(self.order) + 7) // 8])


        def sign(self, subject, private_key, recoverable, is_compressed, entropy):
            z = self._subject_to_bn(subject)
            private_key = BN(private_key)
            k = BN(entropy)

            rp = lib.EC_POINT_new(self.group)
            try:
                # Fix Minerva
                k1 = k + self.order
                k2 = k1 + self.order
                if len(k1) == len(k2):
                    k = k2
                else:
                    k = k1
                if not lib.EC_POINT_mul(self.group, rp, k.bn, None, None, None):
                    raise ValueError("Could not generate R")
                # Convert to affine coordinates
                rx = BN()
                ry = BN()
                if lib.EC_POINT_get_affine_coordinates_GFp(self.group, rp, rx.bn, ry.bn, None) != 1:
                    raise ValueError("Failed to convert R to affine coordinates")
                r = rx % self.order
                if r == BN(0):
                    raise ValueError("Invalid k")
                # Calculate s = k^-1 * (z + r * private_key) mod n
                s = (k.inverse(self.order) * (z + r * private_key)) % self.order
                if s == BN(0):
                    raise ValueError("Invalid k")
                r_buf = r.bytes(self.public_key_length)
                s_buf = s.bytes(self.public_key_length)
                if recoverable:
                    # Generate recid
                    recid = (int(ry % BN(2)))
                    # The line below is highly unlikely to matter in case of
                    # secp256k1 but might make sense for other curves
                    recid += 2 * int(rx // self.order)
                    if is_compressed:
                        return bytes([31 + recid]) + r_buf + s_buf
                    else:
                        if recid >= 4:
                            raise ValueError("Too big recovery ID, use compressed address instead")
                        return bytes([27 + recid]) + r_buf + s_buf
                else:
                    return r_buf + s_buf
            finally:
                lib.EC_POINT_free(rp)


        def recover(self, signature, subject):
            recid = signature[0] - 27 if signature[0] < 31 else signature[0] - 31
            r = BN(signature[1:self.public_key_length + 1])
            s = BN(signature[self.public_key_length + 1:])

            # Verify bounds
            if r >= self.order:
                raise ValueError("r is out of bounds")
            if s >= self.order:
                raise ValueError("s is out of bounds")

            z = self._subject_to_bn(subject)

            rinv = r.inverse(self.order)
            u1 = (-z * rinv) % self.order
            u2 = (s * rinv) % self.order

            # Recover R
            rx = r + BN(recid // 2) * self.order
            if rx >= self.p:
                raise ValueError("Rx is out of bounds")
            ry_mod = recid % 2
            rp = lib.EC_POINT_new(self.group)
            if not rp:
                raise ValueError("Could not create R")
            try:
                init_buf = b"\x02" + rx.bytes(self.public_key_length)
                if not lib.EC_POINT_oct2point(self.group, rp, init_buf, len(init_buf), None):
                    raise ValueError("Could not use Rx to initialize point")
                ry = BN()
                if lib.EC_POINT_get_affine_coordinates_GFp(self.group, rp, None, ry.bn, None) != 1:
                    raise ValueError("Failed to convert R to affine coordinates")
                if int(ry % BN(2)) != ry_mod:
                    # Fix Ry sign
                    ry = self.p - ry
                    if lib.EC_POINT_set_affine_coordinates_GFp(self.group, rp, rx.bn, ry.bn, None) != 1:
                        raise ValueError("Failed to update R coordinates")

                # Recover public key
                result = lib.EC_POINT_new(self.group)
                if not result:
                    raise ValueError("Could not create point")
                try:
                    if not lib.EC_POINT_mul(self.group, result, u1.bn, rp, u2.bn, None):
                        raise ValueError("Could not recover public key")
                    return self._point_to_affine(result)
                finally:
                    lib.EC_POINT_free(result)
            finally:
                lib.EC_POINT_free(rp)


        def verify(self, signature, subject, public_key):
            r_raw = signature[:self.public_key_length]
            r = BN(r_raw)
            s = BN(signature[self.public_key_length:])
            if r >= self.order:
                raise ValueError("r is out of bounds")
            if s >= self.order:
                raise ValueError("s is out of bounds")

            z = self._subject_to_bn(subject)

            pub_p = lib.EC_POINT_new(self.group)
            if not pub_p:
                raise ValueError("Could not create public key point")
            try:
                init_buf = b"\x04" + public_key[0] + public_key[1]
                if not lib.EC_POINT_oct2point(self.group, pub_p, init_buf, len(init_buf), None):
                    raise ValueError("Could initialize point")

                sinv = s.inverse(self.order)
                u1 = (z * sinv) % self.order
                u2 = (r * sinv) % self.order

                # Recover public key
                result = lib.EC_POINT_new(self.group)
                if not result:
                    raise ValueError("Could not create point")
                try:
                    if not lib.EC_POINT_mul(self.group, result, u1.bn, pub_p, u2.bn, None):
                        raise ValueError("Could not recover public key")
                    if BN(self._point_to_affine(result)[0]) % self.order != r:
                        raise ValueError("Invalid signature")
                    return True
                finally:
                    lib.EC_POINT_free(result)
            finally:
                lib.EC_POINT_free(pub_p)


        def derive_child(self, seed, child):
            # Round 1
            h = hmac.new(key=b"Bitcoin seed", msg=seed, digestmod="sha512").digest()
            private_key1 = h[:32]
            x, y = self.private_to_public(private_key1)
            public_key1 = bytes([0x02 + (y[-1] % 2)]) + x
            private_key1 = BN(private_key1)

            # Round 2
            child_bytes = []
            for _ in range(4):
                child_bytes.append(child & 255)
                child >>= 8
            child_bytes = bytes(child_bytes[::-1])
            msg = public_key1 + child_bytes
            h = hmac.new(key=h[32:], msg=msg, digestmod="sha512").digest()
            private_key2 = BN(h[:32])

            return ((private_key1 + private_key2) % self.order).bytes(self.public_key_length)


class RSA:
    pass


aes = AES()
ecc = ECC(ECCBackend(), aes)
rsa = RSA()
