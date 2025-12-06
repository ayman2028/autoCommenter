# Auto Commenter - Local LLM-Powered Code Commenting Tool

Automatically generate helpful comments for your code using a **locally running LLM** (no cloud API, completely private).

## Features

- 🖥️ **Runs Locally**: Uses Ollama or LLaMA.cpp - no external API calls
- 🔒 **Private**: All processing happens on your computer
- 📁 **Multi-Language Support**: Works with Python, JavaScript, TypeScript, Java, C++, C#, Go, Ruby, and more
- 📄 **Single File or Batch**: Process individual files or entire directories
- 🎯 **Smart Commenting**: Adds comments to functions, classes, and complex logic without over-commenting
- ⚡ **Fast**: Runs on your hardware (GPU/CPU)
- 🤖 **Auto Model Detection**: Automatically finds and uses the most powerful available LLM
- ☁️ **Cloud Fallback**: Optional fallback to cloud APIs (OpenAI, etc.) if no local models available
- 🎯 **Zero Configuration**: Just run it - auto-configures everything!

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

## How It Works

The auto-commenter uses an intelligent priority system:

```
1. Detect local Ollama installation
   ↓
2. Find all available models
   ↓
3. Select the most powerful model (dolphin-mixtral > mistral > llama2, etc.)
   ↓
4. Use that model for commenting
   ↓
5. If no local models → Fall back to cloud API (if configured)
```

**No manual model selection needed!** The script automatically chooses the best option.

## Configuration

The `config.json` file controls all settings (but defaults work great!):

```json
{
  "llm_provider": "ollama",                    // Primary LLM provider
  "api_endpoint": "http://localhost:11434",   // Local Ollama endpoint
  "model": "auto",                            // Auto-detects best model
  "temperature": 0.3,                         // 0.0-1.0 (lower = consistent)
  "max_tokens": 2000,                         // Max response length
  "cloud_api_key": "",                        // Optional: OpenAI API key for fallback
  "cloud_model": "gpt-3.5-turbo",            // Cloud model to use if local unavailable
  "supported_extensions": [...]               // File types to process
}
```

### Priority Order

1. **Local Ollama** (Preferred - Private, Fast)
   - Automatically detects installed models
   - Selects the most powerful one
   
2. **Cloud API** (Fallback - Add API key to config.json)
   - OpenAI, Anthropic, or other providers
   - Only used if no local models available

3. **Error** (No LLM available)
   - Clear error message with setup instructions

## Usage

### Quick Start (3 steps!)

**Step 1: Start Ollama**
```bash
ollama serve
```

**Step 2: In another terminal, run the script**
```bash
pipenv run python auto_commenter.py script.py
```

**Step 3: Done!** Your commented code is in `script_commented.py`

The script automatically:
- ✅ Connects to Ollama
- ✅ Finds available models
- ✅ Selects the best one
- ✅ Generates comments

**No configuration needed!**

### Advanced Usage

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
