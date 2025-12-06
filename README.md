# Auto Commenter - Local LLM-Powered Code Commenting Tool

Automatically generate helpful comments for your code using a **locally running LLM** (no cloud API, completely private).

## Features

- 🖥️ **Runs Locally**: Uses Ollama or LLaMA.cpp - no external API calls
- 🔒 **Private**: All processing happens on your computer
- 📁 **Multi-Language Support**: Works with Python, JavaScript, TypeScript, Java, C++, C#, Go, Ruby, and more
- 📄 **Single File or Batch**: Process individual files or entire directories
- 🎯 **Smart Commenting**: Adds comments to functions, classes, and complex logic without over-commenting
- ⚡ **Fast**: Runs on your hardware (GPU/CPU)

## Prerequisites

Choose one of the following local LLM options:

### Option 1: Ollama (Recommended - Easiest)

1. Download Ollama from: https://ollama.ai
2. Install and run it
3. Open a terminal and run:
```bash
ollama serve
```

4. In another terminal, pull a model (one-time setup):
```bash
ollama pull mistral
```

Other available models:
- `ollama pull llama2` - Meta's Llama 2 (larger, more capable)
- `ollama pull neural-chat` - Intel's optimized model
- `ollama pull orca-mini` - Smaller, faster model
- `ollama pull dolphin-mixtral` - Mixture of experts model

### Option 2: LLaMA.cpp

1. Clone the repository: https://github.com/ggerganov/llama.cpp
2. Follow their build instructions
3. Download a GGUF format model
4. Run the server

## Installation

### With Pipenv (Recommended - Isolated Environment)

1. Clone or download this project
2. Install Pipenv (if not already installed):
```bash
pip install pipenv
```

3. Set up the project with Pipenv:
```bash
cd "d:\Documents\Beckend projects\autoCommenter"
pipenv install
```

4. The `config.json` file will be auto-created on first run with default settings for Ollama

### Without Pipenv (Using pip directly)

1. Clone or download this project
2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. The `config.json` file will be auto-created on first run with default settings for Ollama

## Configuration

The `config.json` file controls all settings:

```json
{
  "llm_provider": "ollama",           // "ollama" or "llamacpp"
  "api_endpoint": "http://localhost:11434",  // Local LLM endpoint
  "model": "mistral",                 // Model name to use
  "temperature": 0.3,                 // 0.0-1.0 (lower = more consistent)
  "max_tokens": 2000,                 // Max response length
  "supported_extensions": [...]       // File types to process
}
```

## Usage

### Step 1: Start your local LLM

**For Ollama:**
```bash
ollama serve
```

### Step 2: In another terminal, use Auto Commenter

#### Using Pipenv (Recommended)

**Option A: Activate the virtual environment**
```bash
pipenv shell
python auto_commenter.py <file_or_directory>
exit
```

**Option B: Run without activating**
```bash
pipenv run python auto_commenter.py <file_or_directory>
```

**Option C: Use built-in scripts**
```bash
pipenv run test          # Test with example.py
pipenv run comment script.py
```

#### Without Pipenv

```bash
python auto_commenter.py <file_or_directory>
```

### Examples

**Comment a single file:**
```bash
pipenv run python auto_commenter.py script.py
```
Creates `script_commented.py` with added comments.

**Comment and specify output file:**
```bash
pipenv run python auto_commenter.py script.py output.py
```

**Comment all files in a directory:**
```bash
pipenv run python auto_commenter.py ./src/
```

## Supported Languages

- Python (.py)
- JavaScript (.js)
- TypeScript (.ts, .tsx)
- Java (.java)
- C++ (.cpp)
- C (.c)
- C# (.cs)
- Go (.go)
- Ruby (.rb)
- Kotlin (.kt)
- Rust (.rs)
- Swift (.swift)
- PHP (.php)

## Example

### Before:
```python
def calculate_total(items):
    total = 0
    for item in items:
        total += item.price * item.quantity
    return total
```

### After:
```python
def calculate_total(items):
    """Calculate the total cost of all items.
    
    Args:
        items: List of item objects with price and quantity attributes
        
    Returns:
        Total cost of all items
    """
    total = 0
    # Iterate through each item and accumulate total cost
    for item in items:
        total += item.price * item.quantity
    return total
```

## Troubleshooting

### "Error connecting to local LLM"
- Make sure Ollama is running: `ollama serve`
- Check the API endpoint in `config.json` is correct (default: `http://localhost:11434`)
- Try accessing `http://localhost:11434/api/tags` in your browser

### "Model not found"
- Pull the model: `ollama pull mistral`
- List available models: `ollama list`
- Update the `model` in `config.json`

### Slow performance
- Using a large model on CPU? Try a smaller model: `orca-mini`
- Enable GPU acceleration in Ollama
- Reduce `max_tokens` in config.json

### Out of memory
- Use a smaller model
- Reduce `max_tokens` in config.json
- Close other applications

## Model Recommendations

| Use Case | Model | Size | Speed |
|----------|-------|------|-------|
| Fast & Light | orca-mini | 1.7GB | Very Fast |
| Balanced | mistral | 4GB | Fast |
| High Quality | llama2 | 7GB | Medium |
| Best Quality | dolphin-mixtral | 26GB | Slower |

## Performance Notes

- First run downloads the model (if not cached)
- Processing speed depends on:
  - Your CPU/GPU power
  - Model size
  - Code file size
  - `temperature` and `max_tokens` settings
- Local processing means no internet connection required after model is downloaded

## Privacy

- ✅ **100% local**: No data sent to external servers
- ✅ **No tracking**: No analytics or telemetry
- ✅ **Open source**: Ollama and LLaMA.cpp are open source
- ✅ **Your data**: You have complete control

## License

MIT License

## Acknowledgments

- [Ollama](https://ollama.ai) - For easy local LLM serving
- [LLaMA.cpp](https://github.com/ggerganov/llama.cpp) - For efficient local inference
- [Mistral AI](https://mistral.ai) - For the excellent Mistral model
