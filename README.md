# EnvMan ⚡

**Secure environment variable manager with encryption and team sharing.**

Stop juggling dozens of `.env` files. Manage them all in one place with military-grade encryption.

## ✨ Features

- 🔐 **AES-256 Encryption** - Your secrets stay secret
- 🌍 **Multiple Environments** - Dev, staging, production, and more
- 👥 **Team Sharing** - Share encrypted env files safely
- 💾 **Auto Backups** - Never lose your configs
- 🔄 **Easy Switching** - One command to change environments
- 📊 **Diff Tool** - Compare environments instantly

## 🚀 Quick Start

**Install:**
```bash
pip install envman
```

**Initialize:**
```bash
envman init
# Enter your master password (used to encrypt all variables)
```

**Add an environment:**
```bash
envman add production
envman add staging
```

**Load variables from existing .env file:**
```bash
envman load production .env
```

**Switch environment:**
```bash
envman use production
# Creates .env file in current directory with production variables
```

## 📖 Commands

### Setup
```bash
envman init                    # Initialize with master password
envman add <name>              # Create new environment
```

### Daily Usage
```bash
envman use <env>               # Switch to environment
envman list                    # Show all environments
envman show <env>              # List variables (hidden by default)
envman show <env> --show-values # Show actual values
```

### Managing Variables
```bash
envman set <env> <KEY>         # Set a variable (prompts for value)
envman load <env> <file>       # Load from .env file
envman export <env>            # Export to .env file
```

### Team Collaboration
```bash
envman share <env> -o team.json        # Export for sharing
envman import team.json                # Import shared environment
```

### Advanced
```bash
envman diff prod staging       # Compare environments
envman backup <env>            # Create backup
```

## 💡 How It Works

### Encryption
- Uses **AES-256-GCM** for encryption
- Master password derives encryption keys using **PBKDF2** (100k iterations)
- Each value encrypted separately with unique salt and nonce
- No plain text stored anywhere

### Storage
- **SQLite database** at `~/.envman/envman.db`
- All values encrypted before storage
- Automatic backups with timestamps
- Fast lookups and comparisons

### Workflow Example

```bash
# 1. Initialize once
envman init

# 2. Create environments
envman add development
envman add production

# 3. Load your existing .env files
envman load development .env.dev
envman load production .env.prod

# 4. Switch between them
cd ~/my-project
envman use development  # Creates .env with dev vars

cd ~/my-other-project
envman use production   # Creates .env with prod vars

# 5. Share with team
envman share production -o prod-config.json
# Send prod-config.json to teammate
# They run: envman import prod-config.json
```

## 🔒 Security Best Practices

1. **Master Password**: Use a strong, unique password
2. **Shared Files**: Already encrypted, but still share securely (not in git)
3. **Backups**: Run `envman backup` before major changes
4. **.gitignore**: Never commit `.env` or `~/.envman/` to version control

## 🏗️ Project Structure

```

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repo
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

MIT License - see LICENSE file

## 🙏 Why EnvMan?

Managing environment variables is painful:
- ❌ Scattered `.env` files across projects
- ❌ Manually copying configs between machines
- ❌ Accidentally committing secrets to git
- ❌ Forgetting which values go where

EnvMan solves all of this:
- ✅ One secure database for all environments
- ✅ Encrypted storage of all secrets
- ✅ Easy switching between environments
- ✅ Safe team sharing

---

**Made with ❤️ for developers who are tired of `.env` chaos**
