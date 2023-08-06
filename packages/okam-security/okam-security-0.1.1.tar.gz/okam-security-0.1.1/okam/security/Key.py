import os

class Key:

    @staticmethod
    def encode(key: bytes) -> str:
        return 'hex:%s' % (key.hex())

    @staticmethod
    def decode(key: str) -> bytes:
        if key.find('hex:') == 0:
            return bytes.fromhex(key[4:])
        raise RuntimeError('Unable to decode key: "%s".' % (key))

    @staticmethod
    def generate(length: int = 32) -> bytes:
        return os.urandom(length)

    @staticmethod
    def generate_encoded(length: int = 32) -> str:
        return Key.encode(Key.generate(length))
