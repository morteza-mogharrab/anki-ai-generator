# Contributing to Anki AI Generator

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (Python version, OS, etc.)
- Relevant error messages or logs

### Suggesting Features

Feature requests are welcome! Please:
- Check existing issues first to avoid duplicates
- Clearly describe the feature and its benefits
- Explain your use case
- Consider if it might work better as a separate tool/plugin

### Code Contributions

1. **Fork the repository**
   ```bash
   git clone https://github.com/morteza-mogharrab/anki-ai-generator.git
   cd anki-ai-generator
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow existing code style
   - Add comments for complex logic
   - Update documentation if needed

4. **Test your changes**
   - Test with different CSV inputs
   - Verify Anki import works correctly
   - Check that audio generation works (if applicable)

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add: brief description of changes"
   ```

6. **Push and create a Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

## Code Style Guidelines

- Use clear, descriptive variable names
- Add docstrings to functions
- Keep functions focused and single-purpose
- Follow PEP 8 style guidelines for Python
- Comment complex logic or non-obvious decisions

## Areas for Contribution

Here are some ways you could help improve this project:

### Features
- Add support for other AI models (Anthropic Claude, local models, etc.)
- Implement batch processing with resume capability
- Add progress bars for better UX
- Create a GUI interface
- Support for other flashcard formats (CSV export, etc.)
- Multiple language support

### Improvements
- Better error handling and recovery
- Cost estimation before running
- More card templates and styling options
- Configuration file instead of editing code
- Better logging and debugging options

### Documentation
- Video tutorials
- More example use cases
- Troubleshooting guide expansion
- Translation to other languages

### Testing
- Unit tests
- Integration tests
- Test different CSV formats
- Performance benchmarks

## Questions?

Feel free to open an issue for any questions about contributing.

## Code of Conduct

Be respectful and constructive in all interactions. We're all here to learn and build something useful together.
