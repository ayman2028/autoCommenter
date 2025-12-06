# Quick Start Guide - Pipenv Setup

## What is Pipenv?

Pipenv combines `pip` and `virtualenv` to manage project dependencies in a clean, reproducible way. This project now uses Pipenv for:

- ✅ Isolated virtual environment (no conflicts with other projects)
- ✅ Reproducible dependencies (everyone gets the same versions)
- ✅ Easy to use from anywhere once PATH is configured
- ✅ Built-in scripts for common tasks

## Files Created

| File | Purpose |
|------|---------|
| `Pipfile` | Project dependencies and configuration |
| `Pipfile.lock` | Locked versions for reproducibility |
| `autocomment.bat` | Windows batch wrapper (run from anywhere) |
| `autocomment.ps1` | PowerShell wrapper script |
| `SETUP_PATH.md` | Detailed PATH setup instructions |

## Quick Start

### 1. First Time Setup (Already Done!)
```powershell
pipenv install
```

### 2. Run from Project Directory
```powershell
# Activate the virtual environment
cd "d:\Documents\Beckend projects\autoCommenter"
pipenv shell

# Use the tool
python auto_commenter.py example.py

# Exit when done
exit
```

### 3. Run Without Activating (From Anywhere)
```powershell
pipenv run python auto_commenter.py script.py
```

### 4. Using the Wrapper Scripts (After Adding to PATH)
```powershell
# Windows batch
autocomment script.py

# PowerShell
.\autocomment.ps1 script.py
```

## Using Pipenv Commands

```powershell
# Activate virtual environment
pipenv shell

# Run command in virtual environment without entering it
pipenv run python auto_commenter.py script.py

# Install a new package
pipenv install package-name

# Install development dependency
pipenv install --dev package-name

# Update all packages
pipenv update

# Show dependency tree
pipenv graph

# Remove virtual environment
pipenv --rm

# Check for security issues
pipenv check
```

## Making it Global

To use `autocomment` from anywhere:

1. **Windows PATH method** (Recommended):
   - Add `d:\Documents\Beckend projects\autoCommenter` to your Windows PATH
   - Run `autocomment.bat script.py` from anywhere

2. **PowerShell Alias method**:
   - Add to your PowerShell profile:
     ```powershell
     function autocomment { & "d:\Documents\Beckend projects\autoCommenter\autocomment.ps1" @args }
     ```

3. **Direct Pipenv method**:
   - Run: `pipenv run python auto_commenter.py script.py` from any directory

See `SETUP_PATH.md` for detailed instructions.

## Project Structure

```
autoCommenter/
├── auto_commenter.py      # Main script
├── config.py              # Configuration handler
├── setup.py               # Setup helper
├── example.py             # Example code to test
├── config.json            # Configuration file
├── Pipfile                # Pipenv dependencies (replaces requirements.txt)
├── Pipfile.lock           # Locked versions
├── requirements.txt       # Keep for reference (auto-generated)
├── autocomment.bat        # Windows batch wrapper
├── autocomment.ps1        # PowerShell wrapper
├── README.md              # Main documentation
├── SETUP_PATH.md          # PATH setup guide
└── QUICK_START.md         # This file
```

## Next Steps

1. **Test the installation**:
   ```powershell
   cd "d:\Documents\Beckend projects\autoCommenter"
   pipenv run python auto_commenter.py example.py
   ```

2. **Start Ollama** (required for the tool to work):
   ```powershell
   ollama serve
   ```

3. **Use the tool**:
   ```powershell
   pipenv run python auto_commenter.py your_script.py
   ```

4. **Optional: Add to PATH** to use from anywhere (see SETUP_PATH.md)

## Benefits of Pipenv

- **Reproducibility**: Everyone gets the same package versions
- **Security**: Detects vulnerable dependencies
- **Simplicity**: Single `Pipfile` instead of requirements.txt
- **Scripts**: Built-in commands without separate shell scripts
- **Virtual Environment**: Automatically isolated from system Python

## Troubleshooting

**Q: How do I know the virtual environment is active?**
A: Your prompt will show `(autoCommenter-xxx)` prefix

**Q: Can I use this without Pipenv?**
A: Yes, but you'll need to manually manage the `requirements.txt` and virtual environment

**Q: How do I add a new dependency?**
A: Run `pipenv install package-name` and commit the new `Pipfile.lock`

**Q: Where is my virtual environment?**
A: At `C:\Users\<YourUsername>\.virtualenvs\autoCommenter-<hash>\`

For more information, visit: https://pipenv.pypa.io/
