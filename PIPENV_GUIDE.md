# Pipenv Installation & Usage Guide

## What You Have

Your project is now fully configured with Pipenv! Here's what was set up:

- ✅ `Pipfile` - Dependency specification
- ✅ `Pipfile.lock` - Locked versions for reproducibility
- ✅ Virtual environment - Automatically created and managed by Pipenv
- ✅ Wrapper scripts - Run from anywhere (both `.bat` and `.ps1`)
- ✅ Scripts - Shortcuts in Pipfile for common commands

## Installation Status

```
✓ Pipenv installed: version 2025.0.4
✓ Dependencies installed: requests>=2.31.0
✓ Virtual environment created
✓ Wrapper scripts created
✓ Everything ready to use!
```

## How to Use Pipenv

### Method 1: Activate Virtual Environment (Most Common)

```powershell
# Navigate to project
cd "d:\Documents\Beckend projects\autoCommenter"

# Activate the virtual environment
pipenv shell

# Now you can use Python directly
python auto_commenter.py example.py
python setup.py

# Exit the environment when done
exit
```

**Prompt tip**: When activated, your prompt will show `(autoCommenter-xyz)` prefix.

### Method 2: Run Commands Without Activation (Single Command)

Use `pipenv run` to execute a single command:

```powershell
cd "d:\Documents\Beckend projects\autoCommenter"
pipenv run python auto_commenter.py example.py
```

### Method 3: Use Built-in Pipfile Scripts

We've configured shortcuts in the Pipfile:

```powershell
cd "d:\Documents\Beckend projects\autoCommenter"

# Run Auto Commenter
pipenv run comment example.py

# Run setup script
pipenv run setup

# Test with example
pipenv run test
```

### Method 4: Use Wrapper Scripts (Once Added to PATH)

After adding to Windows PATH (see SETUP_PATH.md):

```powershell
# From anywhere, just use:
autocomment script.py
autocomment script.py output.py
```

## Common Pipenv Commands

```powershell
# Show virtual environment info
pipenv --venv

# Show Python location
pipenv run which python

# Install additional package
pipenv install package-name

# Install dev dependency
pipenv install --dev pytest

# Update all packages
pipenv update

# Show dependency tree
pipenv graph

# Remove virtual environment (to recreate fresh)
pipenv --rm

# Recreate environment from Pipfile.lock
pipenv install

# Check for security vulnerabilities
pipenv check

# Generate requirements.txt from Pipfile
pipenv requirements > requirements.txt
```

## Where Are Things Stored?

```
Your Pipenv virtual environment:
C:\Users\<YourUsername>\.virtualenvs\autoCommenter-<random-hash>\

Your project:
d:\Documents\Beckend projects\autoCommenter\
```

The virtual environment is automatically managed by Pipenv - you don't need to touch it!

## Troubleshooting

### "pipenv: command not found"
```powershell
pip install pipenv
```

### "ModuleNotFoundError: No module named 'requests'"
- Make sure you're using `pipenv shell` or `pipenv run`
- Or run: `pipenv install requests`

### Virtual environment not activating
```powershell
# Recreate it
pipenv --rm
pipenv install
```

### Want to use a different Python version?
```powershell
# Check your Python installations
py --list-paths

# Use specific version
pipenv --python 3.11
pipenv install
```

## Moving/Sharing the Project

**To share with others:**

1. Share these files:
   - `Pipfile` (everyone needs this)
   - `Pipfile.lock` (for exact reproducibility)
   - Your source code files

2. They run:
   ```powershell
   pipenv install
   pipenv run python auto_commenter.py script.py
   ```

Done! Pipenv handles everything.

## Why Pipenv?

| Feature | Pip + Venv | Pipenv |
|---------|-----------|--------|
| Dependency management | ✓ Manual | ✓ Automatic |
| Virtual env isolation | ✓ Manual | ✓ Automatic |
| Lock file | ✗ | ✓ Pipfile.lock |
| Security checks | ✗ | ✓ pipenv check |
| Built-in scripts | ✗ | ✓ Pipfile scripts |
| Reproducibility | Partial | ✓ Perfect |

## Next Steps

1. **Test it works:**
   ```powershell
   cd "d:\Documents\Beckend projects\autoCommenter"
   pipenv run python auto_commenter.py example.py
   ```

2. **Start Ollama** (required for actual use):
   ```powershell
   ollama serve
   ```

3. **Use the tool:**
   ```powershell
   pipenv run python auto_commenter.py your_file.py
   ```

4. **Optional: Add to PATH** for global usage (see SETUP_PATH.md)

## Resources

- Pipenv Documentation: https://pipenv.pypa.io/
- Pipenv GitHub: https://github.com/pypa/pipenv
- PEP 440 (Versioning): https://www.python.org/dev/peps/pep-0440/

---

**You're all set!** Your Auto Commenter is now ready to use with Pipenv's isolated, reproducible environment. 🎉
