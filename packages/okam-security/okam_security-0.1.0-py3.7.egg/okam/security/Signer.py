import hashlib
import hmac

class Signer:

    MAC_LENGTH = 64

    def __init__(self, secret):
        self._secret = secret

    def _get_signature(self, string):
        return hmac.new(self._secret, string.encode('utf-8'), hashlib.sha256).hexdigest()

    def sign(self, string):
        return '%s%s' % (self._get_signature(string), string)

    def validate(self, string):
        validated = string[self.MAC_LENGTH:]

        if hmac.compare_digest(self._get_signature(validated), string[:self.MAC_LENGTH]):
            return validated
        return False
