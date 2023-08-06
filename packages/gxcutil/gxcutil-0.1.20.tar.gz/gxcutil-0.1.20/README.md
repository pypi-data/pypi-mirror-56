# GXCUtil

GXCUtil is a Python utility library for GXC.

## Installation

```
$ pip install gxcutil
```

## Utilities

GXCUtil includes several pure Python (exclude AES) utility functions.

- `ecc` - Pure python ECC methods. Supports Secp256k1 and wNAF caching implemented.
- `aes.py` - AES encrypt/decrypt
- `base58.py` - Base58 encode/decode
- `client.py` - Django request IP parser
- `hash.py` - A few hash functions
- `key.py` - GXC private/public key converter
- `serialize.py` - GXC transaction serializer
- `utils.py` - etc.

## Caution

This repository is implemented and maintained for internal use only.
Please use GXCUtil on your own risk.

## License

[MIT](./LICENSE)
