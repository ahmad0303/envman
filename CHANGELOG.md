# Changelog

All notable changes to EnvMan will be documented in this file.

## [1.0.0] - 2024-03-24

### Added
- Initial release
- AES-256-GCM encryption for all variables
- Multiple environment support
- CLI commands: init, add, list, use, set, show, export, load
- Team sharing with encrypted export/import
- Environment comparison (diff)
- Automatic backups
- SQLite storage backend
- PBKDF2 key derivation (100k iterations)

### Security
- All values encrypted before storage
- Master password never stored in plain text
- Unique salt and nonce for each encryption
- Secure key derivation

### Documentation
- Comprehensive README
- Contributing guide
- Example usage scripts
- MIT License
