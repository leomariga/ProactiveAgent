## Contributing to ProactiveAgent

We love your input! We want to make contributing as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Setup

This project uses [uv](https://docs.astral.sh/uv/) for fast, reliable dependency management.

### Prerequisites

Install uv if you haven't already:

```bash
pip install uv
```

Or follow the [official installation guide](https://docs.astral.sh/uv/getting-started/installation/).

### Setting Up Your Development Environment

1. **Fork and clone the repository:**

```bash
git clone https://github.com/YOUR_USERNAME/ProactiveAgent.git
cd ProactiveAgent
```

2. **Install dependencies:**

```bash
# Install all dependencies including dev tools
uv sync --dev
```

This will:
- Create a virtual environment automatically
- Install all project dependencies from `uv.lock`
- Install development dependencies (linters, formatters, testing tools)

3. **Run examples or tests:**

```bash
# Run any script using uv
uv run python examples/minimal_chat.py

# Or activate the virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
python examples/minimal_chat.py
```

### Development Dependencies

The `--dev` flag installs additional tools for development:
- Code formatters and linters
- Testing frameworks
- Documentation generators
- Any other development utilities

To see all installed dependencies:

```bash
uv pip list
```

## We develop with GitHub
We use GitHub to host code, track issues and feature requests, and accept pull requests.

## We use GitHub Flow, so all code changes happen through pull requests
We actively welcome your pull requests:

1. Fork the repo and create a new branch from `main`.
2. Make focused changes and update documentation when needed.
3. Ensure your code lints/formats locally (see `pyproject.toml` if tools are configured).
4. Open a pull request with a clear title and description.
5. Respond to review feedback and keep your branch up to date with `main`.

## Report bugs using GitHub issues
Use issues to track public bugs and requests. Open a new issue here: [ProactiveAgent issues](https://github.com/leomariga/ProactiveAgent/issues).

## Write bug reports with detail, background, and sample code
Great bug reports include:

- A quick summary and background
- Steps to reproduce (be specific!) with minimal sample code if possible
- What you expected to happen
- What actually happened
- Notes (why this might be happening, things you tried)

## Use a consistent coding style
- 4 spaces for indentation
- Follow existing patterns and prefer clear, descriptive names
- Run configured linters/formatters before committing (see `pyproject.toml`)
- Add concise docstrings where helpful

## License
By contributing, you agree that your contributions will be licensed under the repository's BSD 3‑Clause License. See [`LICENSE`](./LICENSE) for details.
