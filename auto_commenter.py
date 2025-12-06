#!/usr/bin/env python3
"""
Auto Commenter - Local LLM-powered code commenting tool
This script uses a local LLM (Ollama or LLaMA.cpp) to automatically generate comments for code files.
"""

import os
import sys
from pathlib import Path
from typing import Optional, List, Dict
import requests
import json
from config import Config


class LocalLLMAnalyzer:
    """Analyzes code and generates comments using a local LLM."""
    
    # Model rankings (higher = more powerful)
    MODEL_RANKINGS = {
        'dolphin-mixtral': 10,
        'dolphin2.2-mistral': 9,
        'mistral': 8,
        'llama2': 7,
        'neural-chat': 6,
        'orca-mini': 5,
        'vicuna': 4,
        'default': 1,
    }
    
    def __init__(self, config: Config):
        """Initialize the code analyzer with local LLM configuration."""
        self.config = config
        self.api_endpoint = config.get_api_endpoint()
        self.available_models = []
        self.model = None
        self.use_local = True
        
        # Try local LLM first
        if self.verify_connection():
            self.detect_available_models()
            if self.available_models:
                self.select_best_model()
            else:
                print("\n✗ No local models found")
                print("  Try: ollama pull mistral")
                sys.exit(1)
        else:
            # Fall back to cloud API if local not available
            print("\n⚠ Could not connect to local Ollama")
            self.try_cloud_api()
    
    def try_cloud_api(self) -> bool:
        """Try to use cloud API if local LLM is not available."""
        cloud_api_key = self.config.get_cloud_api_key()
        
        if cloud_api_key:
            self.use_local = False
            print("✓ Falling back to cloud API")
            self.model = "gpt-3.5-turbo"  # or configured cloud model
            return True
        else:
            print("✗ No cloud API key configured")
            print("\nTo use cloud API, add your API key to config.json:")
            print('  "cloud_api_key": "your-api-key-here"')
            print("\nOr start Ollama locally:")
            print("  ollama serve")
            sys.exit(1)
    
    def detect_available_models(self) -> List[str]:
        """Detect all available models on the local LLM."""
        try:
            response = requests.get(f"{self.api_endpoint}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                models = data.get('models', [])
                self.available_models = [m.get('name', '').split(':')[0] for m in models]
                
                if self.available_models:
                    print(f"✓ Found {len(self.available_models)} model(s): {', '.join(self.available_models)}")
                else:
                    print("✗ No models found. Please download a model first: ollama pull mistral")
                    sys.exit(1)
                
                return self.available_models
        except Exception as e:
            print(f"Error detecting models: {e}")
            sys.exit(1)
    
    def select_best_model(self) -> str:
        """Select the most powerful model from available options."""
        if not self.available_models:
            print("No models available")
            sys.exit(1)
        
        # Sort models by their ranking
        ranked_models = []
        for model in self.available_models:
            rank = self.MODEL_RANKINGS.get(model, 1)
            ranked_models.append((model, rank))
        
        ranked_models.sort(key=lambda x: x[1], reverse=True)
        best_model = ranked_models[0][0]
        
        print(f"✓ Selected model: {best_model} (most powerful available)")
        self.model = best_model
        return best_model
    
    def verify_connection(self) -> bool:
        """Verify connection to the local LLM."""
        try:
            response = requests.get(f"{self.api_endpoint}/api/tags", timeout=5)
            if response.status_code == 200:
                print(f"✓ Connected to local LLM at {self.api_endpoint}")
                return True
            else:
                print(f"✗ Ollama returned status {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Error connecting to local LLM: {e}")
            print(f"  Make sure Ollama is running: ollama serve")
            return False
    
    def read_file(self, file_path: str) -> str:
        """Read the contents of a code file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return ""
    
    def write_file(self, file_path: str, content: str) -> bool:
        """Write the commented code to a file."""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error writing file {file_path}: {e}")
            return False
    
    def get_file_type(self, file_path: str) -> str:
        """Determine the programming language from file extension."""
        extension_map = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.jsx': 'JavaScript',
            '.tsx': 'TypeScript',
            '.java': 'Java',
            '.cpp': 'C++',
            '.c': 'C',
            '.cs': 'C#',
            '.go': 'Go',
            '.rb': 'Ruby',
            '.php': 'PHP',
            '.swift': 'Swift',
            '.kt': 'Kotlin',
            '.rs': 'Rust',
        }
        ext = Path(file_path).suffix.lower()
        return extension_map.get(ext, 'Unknown')
    
    def generate_comments(self, code: str, language: str) -> str:
        """Generate comments for code using local or cloud LLM."""
        if self.use_local:
            return self._generate_local(code, language)
        else:
            return self._generate_cloud(code, language)
    
    def _generate_local(self, code: str, language: str) -> str:
        """Generate comments using local LLM via Ollama."""
        try:
            prompt = f"""You are an expert code commenter. Your task is to add helpful comments to the following {language} code.

Rules:
1. Add comments above functions, classes, and complex logic blocks
2. Explain the purpose and parameters of functions
3. Keep comments concise but informative
4. Use single-line comments for simple statements
5. Use multi-line comments for complex sections
6. Don't over-comment obvious code
7. Preserve the original code structure exactly

{language} Code to comment:
```
{code}
```

Return ONLY the commented code, nothing else. Do not add markdown formatting or code blocks."""

            response = requests.post(
                f"{self.api_endpoint}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "temperature": self.config.get_temperature(),
                    "num_predict": self.config.get_max_tokens(),
                },
                timeout=300  # 5 minutes timeout for local processing
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', code).strip()
            else:
                print(f"Error from LLM: {response.status_code}")
                return code
                
        except Exception as e:
            print(f"Error generating comments with local LLM: {e}")
            return code
    
    def _generate_cloud(self, code: str, language: str) -> str:
        """Generate comments using cloud API (OpenAI, etc.)."""
        try:
            import openai
            
            api_key = self.config.get_cloud_api_key()
            if not api_key:
                print("No cloud API key configured")
                return code
            
            openai.api_key = api_key
            
            prompt = f"""You are an expert code commenter. Add helpful comments to this {language} code:

{code}

Return ONLY the commented code, nothing else."""
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert code commenter."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.config.get_temperature(),
                max_tokens=self.config.get_max_tokens(),
            )
            
            return response.choices[0].message.content.strip()
            
        except ImportError:
            print("OpenAI package not installed. Run: pip install openai")
            return code
        except Exception as e:
            print(f"Error generating comments with cloud API: {e}")
            return code
    
    def process_file(self, input_file: str, output_file: Optional[str] = None) -> bool:
        """Process a code file and add AI-generated comments."""
        if not os.path.exists(input_file):
            print(f"File not found: {input_file}")
            return False
        
        if output_file is None:
            base, ext = os.path.splitext(input_file)
            output_file = f"{base}_commented{ext}"
        
        print(f"\nReading file: {input_file}")
        code = self.read_file(input_file)
        
        if not code:
            print("File is empty or couldn't be read.")
            return False
        
        language = self.get_file_type(input_file)
        print(f"Detected language: {language}")
        print(f"Using model: {self.model}")
        print("Generating comments with local LLM (this may take a moment)...")
        
        commented_code = self.generate_comments(code, language)
        
        print(f"Writing commented code to: {output_file}")
        success = self.write_file(output_file, commented_code)
        
        if success:
            print("✓ Successfully commented the code!")
        
        return success
    
    def process_directory(self, directory: str, extensions: Optional[list] = None) -> None:
        """Process all code files in a directory."""
        if extensions is None:
            extensions = ['.py', '.js', '.ts', '.java', '.cpp']
        
        print(f"Processing directory: {directory}")
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    file_path = os.path.join(root, file)
                    print(f"\nProcessing: {file_path}")
                    self.process_file(file_path)


def main():
    """Main entry point for the script."""
    if len(sys.argv) < 2:
        print("Usage: python auto_commenter.py <file_or_directory> [output_file]")
        print("\nExample:")
        print("  python auto_commenter.py script.py")
        print("  python auto_commenter.py script.py output_script.py")
        print("  python auto_commenter.py ./src/")
        print("\nRequirements:")
        print("  - Ollama running locally: ollama serve")
        print("  - At least one model downloaded: ollama pull mistral")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Load configuration
    config = Config()
    
    # Create analyzer (handles connection, model detection, and selection)
    analyzer = LocalLLMAnalyzer(config)
    
    if os.path.isfile(input_path):
        analyzer.process_file(input_path, output_file)
    elif os.path.isdir(input_path):
        analyzer.process_directory(input_path)
    else:
        print(f"Invalid path: {input_path}")
        sys.exit(1)


if __name__ == "__main__":
    main()
