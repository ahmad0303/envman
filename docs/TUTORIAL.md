# Quick Start Tutorial

Get up and running with EnvMan in 5 minutes.

## Installation

```bash
git clone https://github.com/yourusername/envman.git
cd envman
pip install envman
```

## Tutorial: Managing Dev & Prod Environments

### Step 1: Initialize EnvMan

```bash
envman init
```

**Prompt:** Enter master password
**Choose:** A strong password (you'll need this forever!)

Example: `MySecurePass123!@#`

✅ **What happened?** EnvMan created `~/.envman/envman.db` with your encrypted config.

---

### Step 2: Create Environments

```bash
envman add development
envman add production
envman add staging
```

✅ **What happened?** Three environments created in the database.

Check them:
```bash
envman list
```

---

### Step 3: Load Your Existing .env Files

Let's say you have these files:
- `.env.development` - 10 variables
- `.env.production` - 10 variables

```bash
# Load development
envman load development .env.development

# Load production
envman load production .env.production
```

✅ **What happened?** All variables encrypted and stored securely.

---

### Step 4: Use an Environment

```bash
# Go to your project
cd ~/my-awesome-app

# Use development environment
envman use development
```

✅ **What happened?** Created `.env` file with all development variables.

Your app can now read from `.env`:
```python
# app.py
from dotenv import load_dotenv
import os

load_dotenv()
print(os.getenv('DATABASE_URL'))  # Works!
```

---

### Step 5: Add a New Variable

```bash
envman set production STRIPE_KEY
```

**Prompt:** Enter value (hidden)
**Type:** `sk_live_abc123...`

✅ **What happened?** Value encrypted and stored in production environment.

---

### Step 6: View Variables

```bash
# List keys only
envman show development

# Show actual values
envman show development --show-values
```

Output:
```
DEVELOPMENT (10 variables)

Key                Value
-----------------  --------
API_KEY            ••••••••
DATABASE_URL       ••••••••
DEBUG              ••••••••
...
```

---

### Step 7: Compare Environments

```bash
envman diff development production
```

Output:
```
Comparing: development ↔ production

Only in development:
  - TEST_MODE

Only in production:
  + STRIPE_KEY

Different values:
  ≠ DATABASE_URL
  ≠ DEBUG

✓ 8 variables are identical
```

---

### Step 8: Share with Team

```bash
# Export production for teammate
envman share production -o prod-config.json
```

**Send** `prod-config.json` to teammate (via Slack, email, etc.)

**Your teammate does:**
```bash
# They initialize (using SAME password you gave them)
envman init
Enter password: MySecurePass123!@#

# Import your shared config
envman import prod-config.json

# Now they have production environment!
envman use production
```

✅ **What happened?** Secure sharing via encrypted export.

---

### Step 9: Switch Projects Quickly

```bash
# Project A needs development
cd ~/project-a
envman use development

# Project B needs production
cd ~/project-b
envman use production

# Project C needs staging
cd ~/project-c
envman use staging
```

✅ **What happened?** Each project has correct `.env` instantly!

---

### Step 10: Backup Before Changes

```bash
# Before updating production
envman backup production

# Make changes
envman set production DATABASE_URL
# Enter new value...

# If something breaks, you have backup!
```

---

## Common Workflows

### New Project Setup

```bash
# 1. Create environment
envman add myproject-dev

# 2. Set variables one by one
envman set myproject-dev DATABASE_URL
envman set myproject-dev API_KEY
envman set myproject-dev SECRET_KEY

# 3. Use it
cd ~/myproject
envman use myproject-dev
```

### Migrating from .env Files

```bash
# You have: .env, .env.local, .env.production
envman add local
envman add production

envman load local .env.local
envman load production .env.production

# Delete old files (now safely in EnvMan)
rm .env.local .env.production
```

### Team Onboarding

**Team Lead:**
```bash
envman share production -o prod.json
envman share staging -o staging.json
# Share files + master password (securely!)
```

**New Developer:**
```bash
envman init  # Use team's master password
envman import prod.json
envman import staging.json
envman list  # See all environments
```

---

## Pro Tips

### 1. Export for Local Backup

```bash
# Export as readable .env file
envman export production -o backup.env
# Store backup.env in password manager
```

### 2. Quick Environment Check

```bash
# See what's in production
envman show production

# Compare with what you have locally
cat .env
```

### 3. Update Multiple Variables

```bash
# Create temp .env with new values
nano updates.env

# Load into environment
envman load production updates.env
```

### 4. Shell Aliases

Add to `~/.bashrc`:
```bash
alias edev="envman use development"
alias eprod="envman use production"
alias elist="envman list"
```

Now:
```bash
edev   # Switch to development
eprod  # Switch to production
```

---

## Troubleshooting

### "EnvMan not initialized"
```bash
envman init  # Set master password
```

### "Environment not found"
```bash
envman list  # Check available environments
envman add myenv  # Create it
```

### "Wrong password"
```bash
# Unfortunately, if you forget the master password,
# encrypted data cannot be recovered.
# This is by design for security.

# Start fresh:
rm -rf ~/.envman
envman init  # Set new password
```

### Variables Not Loading in App
```bash
# Ensure .env exists
ls -la .env

# Check contents
cat .env

# Re-run use command
envman use production
```

---

## Next Steps

- Read [ARCHITECTURE.md](ARCHITECTURE.md) to understand how it works
- Check [CONTRIBUTING.md](../CONTRIBUTING.md) to add features
- Star the repo if this helped you! ⭐

---

**You're now an EnvMan expert! 🎉**
