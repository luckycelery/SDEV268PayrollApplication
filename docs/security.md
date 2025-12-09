# Security Module Documentation

Implementing industry-standard password hashing and authentication using **PyNaCl** with the **Argon2id** algorithm.

## External Library: PyNaCl

**PyNaCl** is a Python binding to libsodium, providing modern cryptographic primitives.

1. **Industry Standard**: Argon2 won the Password Hashing Competition (2015)
2. **OWASP Recommended**: Current best practice for password storage
3. **Memory-Hard**: Resistant to GPU and ASIC brute-force attacks
4. **Built-in Security**: Automatic salt generation, no collision risk
5. **Modern**: More secure than bcrypt or PBKDF2

## Testing

Security tests located in `tests/test_auth.py`:

- Argon2id hash format validation
- Password verification correctness
- Unique salt generation
- Input sanitization
- Authentication flow

Run tests:
```bash
pytest tests/test_auth.py -v
```

## References

- [PyNaCl Documentation](https://pynacl.readthedocs.io/en/latest/password_hashing/)
- [Argon2 Specification](https://github.com/P-H-C/phc-winner-argon2)
- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
