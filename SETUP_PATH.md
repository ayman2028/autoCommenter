# Adding Auto Commenter to Your PATH

This guide helps you use `autocomment` from anywhere on your system.

## Windows Setup

### Option 1: Add to PATH (Recommended)

1. Find the full path to your `autoCommenter` folder:
   ```powershell
   cd "d:\Documents\Beckend projects\autoCommenter"
   pwd  # This shows the full path
   ```

2. Add to Windows PATH:
   - Press `Win + X` and select "System" (or search "Edit environment variables")
   - Click "Environment Variables"
   - Under "User variables", click "New..."
   - Variable name: `PATH`
   - Variable value: `d:\Documents\Beckend projects\autoCommenter`
   - Click OK on all dialogs

3. Restart PowerShell/Command Prompt

4. Now you can run from anywhere:
   ```powershell
   autocomment script.py
   autocomment script.py output.py
   ```

### Option 2: Create a Batch File Shortcut

1. Copy `autocomment.bat` to a folder in your PATH (e.g., `C:\Users\<YourUsername>\AppData\Local\Programs`)

2. Restart your terminal

### Option 3: Create an Alias (PowerShell)

Add this to your PowerShell profile (`$PROFILE`):

```powershell
function autocomment {
    & "d:\Documents\Beckend projects\autoCommenter\autocomment.ps1" @args
}
```

Then restart PowerShell.

## Usage Examples

Once added to PATH:

```powershell
# Comment a single file
autocomment script.py

# Comment with custom output file
autocomment script.py my_commented_script.py

# Comment all files in a directory
autocomment ./src/

# Get help
autocomment --help
```

## Using Pipenv Directly

You can also use Pipenv directly without adding to PATH:

```powershell
# Activate the virtual environment
cd "d:\Documents\Beckend projects\autoCommenter"
pipenv shell

# Now use directly
python auto_commenter.py script.py
python setup.py

# Exit the environment
exit
```

## Using Pipenv Scripts

We've configured convenient scripts in `Pipfile`:

```powershell
cd "d:\Documents\Beckend projects\autoCommenter"

# Run Auto Commenter
pipenv run comment script.py

# Run setup
pipenv run setup

# Test with example
pipenv run test
```

## Troubleshooting

### "Command not found: autocomment"
- Make sure you restarted your terminal after adding to PATH
- Verify the path was added correctly: `$env:PATH` in PowerShell

### "Pipenv not installed"
- Install with: `pip install pipenv`

### "Python not found in virtual environment"
- Recreate the environment: `pipenv --rm` then `pipenv install`

## Virtual Environment Location

Pipenv automatically creates a virtual environment at:
```
C:\Users\<YourUsername>\.virtualenvs\autoCommenter-<hash>\
```

You don't need to manage this - Pipenv handles it automatically!
