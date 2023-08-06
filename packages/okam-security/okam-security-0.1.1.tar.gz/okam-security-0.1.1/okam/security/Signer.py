import hashlib
import hmac

from typing import Union

class Signer:

    MAC_LENGTH = 64

    def __init__(self, key: bytes):
        self._key = key

    def _get_signature(self, string: str) -> str:
        return hmac.new(self._key, string.encode('utf-8'), hashlib.sha256).hexdigest()

    def sign(self, string: str) -> str:
        return '%s%s' % (self._get_signature(string), string)

    def validate(self, string: str) -> Union[str, bool]:
        validated = string[self.MAC_LENGTH:]

        if hmac.compare_digest(self._get_signature(validated), string[:self.MAC_LENGTH]):
            return validated
        return False
