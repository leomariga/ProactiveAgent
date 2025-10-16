# Build and Publish Guide

This guide explains how to build and publish the ProactiveAgent library to PyPI using `uv`.

## Prerequisites

- `uv` package manager installed
- PyPI account and API token
- TestPyPI account (recommended for testing)

## Version Management

### Update Library Version

Update the version of your library in `pyproject.toml`:

```bash
# Patch version (0.1.0 → 0.1.1) - for bug fixes
uv version --bump patch

# Minor version (0.1.0 → 0.2.0) - for new features
uv version --bump minor

# Major version (0.1.0 → 1.0.0) - for breaking changes
uv version --bump major

# Set specific version
uv version 0.2.0
```

## Build Process

### 1. Build the Package

Create distribution files (wheel and source distribution):

```bash
uv build
```

This creates `.whl` and `.tar.gz` files in the `dist/` directory.

### 2. Verify Build

Check what will be included in your package:

```bash
# View built files
ls -la dist/

# Check package contents (if twine is available)
twine check dist/*
```

## Publishing Process



### Publish to Main PyPI

Verify your package works correctly:

```bash
# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ proactiveagent

# Test the installation
python -c "import proactiveagent; print('Installation successful!')"
```

### 3. Publish to Main PyPI

Once tested, publish to the main PyPI:

```bash
uv publish
```

## Complete Workflow

Here's the recommended complete workflow:

```bash
# 1. Update version
uv version --bump minor

# 2. Build package
uv build

# 5. If successful, publish to main PyPI
uv publish
```

## Configuration

The project is already configured with:
- Proper package metadata and classifiers
- Build system using `hatchling`

## Troubleshooting

### Common Issues

1. **Authentication errors**: Ensure your API tokens are correct and have proper permissions
2. **Version conflicts**: Make sure the version doesn't already exist on PyPI
3. **Build errors**: Check that all required files are included in the package

### Check Package Contents

```bash
# See what files will be included
uv build --sdist --wheel
tar -tzf dist/proactiveagent-*.tar.gz | head -20
```

### Validate Before Publishing

```bash
# Check for common issues
python -m build --check
```

## Post-Publication

After successful publication:

1. Verify the package is available on PyPI
2. Test installation: `pip install proactiveagent`
3. Update documentation if needed
4. Create a GitHub release with the same version tag

## Useful Commands

```bash
# Check outdated dependencies
uv tree --outdated

# Upgrade dependencies
uv sync --upgrade

# Clean build artifacts
rm -rf dist/ build/ *.egg-info/

# View package info
uv tree
```