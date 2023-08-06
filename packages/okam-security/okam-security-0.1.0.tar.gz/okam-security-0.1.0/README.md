# Okam Security

[![Build Status](https://img.shields.io/travis/freost/okam-security/master.svg?style=flat)](https://travis-ci.org/freost/okam-security)

A Python port of the [Mako](https://makoframework.com) (PHP framework) security library.

## Usage

### Key

The `Key` class allows you to generate, encode and decode keys that can be used for cryptographic purposes.

```python
from okam.security import Key

# Returns 32 random bytes, you can also pass the number of bytes you want to return

key = Key.generate()

# Returns a hex representation of the random bytes prefixed by 'hex:'

encoded = Key.encode(key)

# Returns the random bytes that were encoded

key = Key.decode(key)

# Returns a hex representation of 32 random bytes prefixed by 'hex:',
# you can also pass the number of bytes you want to return

encoded = Key.generate_encoded()
```

### Signer

The `Signer` class allows you to verify both the data integrity and the authentication of strings. A HMAC (hash-based message authentication code) will be prepended to your string upon signing and stripped when validated.

```python
from okam.security import Key
from okam.security import Signer

signer = Signer(Key.generate())

# Signs the string

signed = signer.sign('hello, world!')

# Returns the original string if the string can be authenticated and False if not

string = signer.validate(signed)
```
