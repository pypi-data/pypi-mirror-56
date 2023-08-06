Saph for Python
===============

Saph is the Stupid Algorithm for Password Hashing. This is the Python 3 implementation.

For more information about Saph, go to [its specification](https://github.com/socram8888/saph/blob/master/README.md).

Usage
-----

The `saph.Saph` class contains the implementation. It may be used as follows:

```python
>>> from saph import Saph
>>> hasher = Saph(memory=16384, iterations=8)
>>> hasher.hash('pepper', 'username', 'password').hex()
'38e48e2b1d4418766568e6212e59abb961b876b2a1f7f269752ed84afe6637c0'
>>> hasher.hash('qepper', 'username', 'password').hex()
'bb4a74eb50bab2e4cd334d93ee85d84f9c91f454ef33a68a484408747f0f391a'
>>> hasher.hash('salt', 'pass').hex()
'e1530ba599f87e4e62560e908f3db833cbefa97dc6cf9100d55df57a3a9e29ad'
```

The `.hash` method accepts strings, bytes and bytearrays.
