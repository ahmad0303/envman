# Contributing to EnvMan

Thanks for your interest in contributing! Here's how you can help:

## Getting Started

1. **Fork** the repository
2. **Clone** your fork:
   ```bash
   git clone https://github.com/ahmad0303/envman.git
   cd envman
   ```
3. **Install** in development mode:
   ```bash
   pip install -e .
   ```

## Development Workflow

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and test them:
   ```bash
   # Test the CLI
   envman --help
   ```

3. Commit with clear messages:
   ```bash
   git commit -m "Add: brief description of what you added"
   ```

4. Push and create a Pull Request:
   ```bash
   git push origin feature/your-feature-name
   ```

## Code Style

- Follow **PEP 8** for Python code
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small

## Testing

Before submitting PR:
- Test all CLI commands manually
- Verify encryption/decryption works
- Check error handling

## Ideas for Contribution

- Add cloud backup integration (AWS S3, Dropbox)
- Implement environment templates
- Add variable validation rules
- Create shell auto-completion
- Improve error messages
- Add more encryption options
- Build GUI interface

## Questions?

Open an issue or reach out to maintainers.

Thank you for contributing! 🎉
