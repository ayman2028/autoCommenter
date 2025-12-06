"""
Configuration handler for Auto Commenter (Local LLM)
Manages local LLM settings and configuration.
"""

import json
import os
from pathlib import Path


class Config:
    """Handles configuration and settings for local LLM."""
    
    def __init__(self, config_file: str = 'config.json'):
        """Initialize configuration from file."""
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self) -> dict:
        """Load configuration from JSON file."""
        if not os.path.exists(self.config_file):
            # Create default config
            return self._create_default_config()
        
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            return self._create_default_config()
    
    def _create_default_config(self) -> dict:
        """Create and save default configuration."""
        default_config = {
            "llm_provider": "ollama",
            "api_endpoint": "http://localhost:11434",
            "model": "mistral",
            "temperature": 0.3,
            "max_tokens": 2000,
            "cloud_api_key": "",
            "cloud_model": "gpt-3.5-turbo",
            "supported_extensions": [
                ".py",
                ".js",
                ".ts",
                ".java",
                ".cpp",
                ".c",
                ".cs",
                ".go",
                ".rb"
            ],
            "notes": [
                "Priority: Local LLM (Ollama) > Cloud API",
                "For local: Install Ollama from https://ollama.ai",
                "For cloud: Add your OpenAI API key to 'cloud_api_key'",
                "Available Ollama models: mistral, llama2, neural-chat, etc.",
                "Pull a model with: ollama pull mistral"
            ]
        }
        
        try:
            with open(self.config_file, 'w') as f:
                json.dump(default_config, f, indent=2)
            print(f"Created default config file: {self.config_file}")
            print("Configuration ready! Make sure your local LLM is running.")
        except Exception as e:
            print(f"Error creating config file: {e}")
        
        return default_config
    
    def get_api_endpoint(self) -> str:
        """Get API endpoint for local LLM."""
        return self.config.get('api_endpoint', 'http://localhost:11434')
    
    def get_model(self) -> str:
        """Get model name from config."""
        return self.config.get('model', 'mistral')
    
    def get_temperature(self) -> float:
        """Get temperature setting from config (0.0 to 1.0)."""
        return self.config.get('temperature', 0.3)
    
    def get_max_tokens(self) -> int:
        """Get max tokens setting from config."""
        return self.config.get('max_tokens', 2000)
    
    def get_supported_extensions(self) -> list:
        """Get list of supported file extensions."""
        return self.config.get('supported_extensions', [])
    
    def get_llm_provider(self) -> str:
        """Get LLM provider type."""
        return self.config.get('llm_provider', 'ollama')
    
    def get_cloud_api_key(self) -> str:
        """Get cloud API key (OpenAI, etc.)."""
        return self.config.get('cloud_api_key', '').strip()
    
    def get_cloud_model(self) -> str:
        """Get cloud model name."""
        return self.config.get('cloud_model', 'gpt-3.5-turbo')
    
    def set_model(self, model: str) -> bool:
        """Set model name and save to config."""
        try:
            self.config['model'] = model
            self.save()
            print(f"Model set to: {model}")
            return True
        except Exception as e:
            print(f"Error setting model: {e}")
            return False
    
    def set_api_endpoint(self, endpoint: str) -> bool:
        """Set API endpoint and save to config."""
        try:
            self.config['api_endpoint'] = endpoint
            self.save()
            print(f"API endpoint set to: {endpoint}")
            return True
        except Exception as e:
            print(f"Error setting API endpoint: {e}")
            return False
    
    def save(self) -> bool:
        """Save current configuration to file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
