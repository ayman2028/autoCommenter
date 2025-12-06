#!/usr/bin/env python3
"""
Setup script for Auto Commenter with local LLM
Helps with installation and configuration.
"""

import sys
import os
import subprocess
from config import Config


def print_header(text):
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")


def check_python():
    """Check Python version."""
    print("Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print(f"✗ Python 3.7+ required, you have {version.major}.{version.minor}")
        return False
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    return True


def install_dependencies():
    """Install required Python packages."""
    print_header("Installing Dependencies")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully")
        return True
    except Exception as e:
        print(f"✗ Error installing dependencies: {e}")
        return False


def setup_ollama():
    """Provide instructions for setting up Ollama."""
    print_header("Ollama Setup Instructions")
    print("""
1. Download Ollama from: https://ollama.ai
2. Install and run the application
3. Open a terminal and run:
   ollama serve

4. In another terminal, pull a model:
   ollama pull mistral

Available models:
   • ollama pull mistral - Fast, recommended for most users
   • ollama pull llama2 - Larger, more capable
   • ollama pull neural-chat - Optimized for chat
   • ollama pull orca-mini - Smallest, fastest
    """)


def test_connection():
    """Test connection to local LLM."""
    print_header("Testing Local LLM Connection")
    
    config = Config()
    endpoint = config.get_api_endpoint()
    model = config.get_model()
    
    print(f"API Endpoint: {endpoint}")
    print(f"Model: {model}")
    
    try:
        import requests
        print("\nAttempting to connect...")
        response = requests.get(f"{endpoint}/api/tags", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            models = data.get('models', [])
            print(f"✓ Successfully connected to Ollama!")
            print(f"\nAvailable models:")
            for m in models:
                print(f"  • {m.get('name', 'unknown')}")
            return True
        else:
            print(f"✗ Connection failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        print(f"\nMake sure Ollama is running:")
        print(f"  ollama serve")
        return False


def main():
    """Main setup flow."""
    print_header("Auto Commenter - Local LLM Setup")
    
    # Check Python
    if not check_python():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n✗ Failed to install dependencies")
        sys.exit(1)
    
    # Show Ollama setup
    setup_ollama()
    
    # Test connection
    input_text = input("\nPress Enter after starting Ollama and pulling a model, or type 'skip' to skip the test: ").strip().lower()
    
    if input_text != 'skip':
        if not test_connection():
            print("\n⚠ Could not connect to local LLM")
            print("Make sure Ollama is running and try again")
        else:
            print("\n✓ Setup complete! You can now use Auto Commenter")
            print("\nNext steps:")
            print("  1. Keep 'ollama serve' running in a terminal")
            print("  2. In another terminal, run: python auto_commenter.py <file>")
    else:
        print("\n✓ Setup skipped connection test")
        print("\nRemember to:")
        print("  1. Start Ollama: ollama serve")
        print("  2. Pull a model: ollama pull mistral")
        print("  3. Run: python auto_commenter.py <file>")


if __name__ == "__main__":
    main()
