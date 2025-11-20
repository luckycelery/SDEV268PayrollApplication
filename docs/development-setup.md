# Development Setup Guide

## For Contributors Using UV

UV is a fast Python package manager that makes dependency management easier.

### Installing UV

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Setting Up the Project

```bash
# Clone the repository
git clone <repo-url>
cd SDEV268PayrollApplication

# Sync dependencies (creates .venv automatically)
uv sync

# Run the database setup
uv run setup_database.py

# Run tests
uv run database/test_database.py
```

### Adding Dependencies

If you need to add a package:

```bash
# Add to main dependencies
uv add package-name

# Add to dev dependencies
uv add --dev package-name

# Add to optional group
uv add --optional enhanced package-name
```

### Running Code

```bash
# Run any Python script
uv run your_script.py

# Or activate the virtual environment
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Then run normally
python your_script.py
```

## For Teammates Using pip

If you prefer pip or don't want to install UV:

### Setup with pip

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Windows CMD:
.venv\Scripts\activate.bat
# Linux/Mac:
source .venv/bin/activate

# Install dev tools (optional)
pip install ruff

# Run scripts normally
python setup_database.py
python database/test_database.py
```

### Keeping Dependencies in Sync

The project uses `pyproject.toml` for UV, but `requirements.txt` is available for pip users.

**If using UV and you add dependencies:**
```bash
# After using `uv add`, export for pip users:
uv pip compile pyproject.toml -o requirements.txt
```

**If using pip:**
Just use `requirements.txt` as normal. Currently, the project has no external dependencies.

## Code Quality with Ruff

### Installation

**With UV:**
```bash
uv sync  # Already includes ruff in dev dependencies
```

**With pip:**
```bash
pip install ruff
```

### Usage

```bash
# Format all code
ruff format .

# Check for issues
ruff check .

# Auto-fix issues where possible
ruff check --fix .

# Check specific file
ruff check database/auth.py
```

### Pre-commit (Optional)

To automatically format code before committing:

```bash
# Create .git/hooks/pre-commit file
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/sh
ruff format .
ruff check --fix .
EOF

# Make executable (Linux/Mac)
chmod +x .git/hooks/pre-commit
```

## Project Configuration

The `pyproject.toml` file contains:
- Project metadata
- Dependency specifications
- Ruff configuration (linting/formatting rules)

Key Ruff settings:
- Line length: 120 characters
- Python target: 3.10+
- Enabled rules: pycodestyle, pyflakes, isort, pyupgrade, bugbear, comprehensions, simplify

## Troubleshooting

### UV Command Not Found

Make sure UV is in your PATH. Restart your terminal after installation.

### Permission Errors

**Windows:** Run PowerShell as Administrator for installation
**Linux/Mac:** Make sure installation script completed successfully

### Ruff Not Found

```bash
# With UV
uv sync

# With pip
pip install ruff
```

### Virtual Environment Issues

Delete `.venv` and recreate:
```bash
rm -rf .venv
uv sync  # or: python -m venv .venv
```

## Resources

- [UV Documentation](https://github.com/astral-sh/uv)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Python Virtual Environments](https://docs.python.org/3/library/venv.html)
