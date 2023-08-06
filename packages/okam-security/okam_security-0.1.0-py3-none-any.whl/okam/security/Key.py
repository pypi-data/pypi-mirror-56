import os

class Key:

    @staticmethod
    def encode(data):
        return 'hex:%s' % (data.hex())

    @staticmethod
    def decode(string):
        if string.find('hex:') == 0:
            return bytes.fromhex(string[4:])
        return string

    @staticmethod
    def generate(length = 32):
        return os.urandom(length)

    @staticmethod
    def generate_encoded(length = 32):
        return Key.encode(Key.generate(length))
