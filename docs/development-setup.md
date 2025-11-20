# Development Setup

## Quick Start

**Setup Project:**

```bash
git clone <repo-url>
cd SDEV268PayrollApplication
python setup_database.py
```

**Run scripts:**

```bash
python your_script.py
```

No external dependencies required (standard library only).

## Alternative: Using UV

**Install UV:**

```powershell
# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Setup Project:**

```bash
uv sync
uv run setup_database.py
```

**Run scripts:**

```bash
uv run your_script.py
```

## Code Formatting with Ruff

**Format code:**

```bash
ruff format .
ruff check --fix .
```

**Ruff settings** (configured in `pyproject.toml`):

- Line length: 120 characters
- Python 3.10+

That's it!
Refer to the [database-setup.md](database-setup) doc for setting up the db schema and testing functionality.
