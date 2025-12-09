#!/usr/bin/env python3
"""
LLM Assistant Library - API calls for coding assistance tasks
Provides utilities for interacting with local LLMs (Ollama) for various coding tasks.
"""

import requests
import json
import os
from pathlib import Path
from typing import Optional, Dict, Any, List
from config import Config


class LLMAssistant:
    """Base class for LLM-powered coding assistance tasks."""
    
    def __init__(self, project_name: Optional[str] = None, config: Optional[Config] = None):
        """
        Initialize the LLM assistant with configuration.
        
        Args:
            project_name: Name of the project (used to load/create training data)
            config: Configuration object (optional)
        """
        self.config = config or Config()
        self.api_endpoint = self.config.get_api_endpoint()
        self.model = self.config.get_model()
        self.project_name = project_name
        self.training_data = None
        
        # Load training data if project name provided
        if project_name:
            self.training_data = self._load_project_training_data(project_name)
        
    def _call_llm(self, prompt: str, temperature: float = 0.3, max_tokens: int = 2000) -> str:
        """
        Make a call to the local LLM API.
        
        Args:
            prompt: The prompt to send to the LLM
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens to generate
            
        Returns:
            The LLM's response as a string
        """
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "temperature": temperature,
                "num_predict": max_tokens,
            }
            
            response = requests.post(
                f"{self.api_endpoint}/api/generate",
                json=payload,
                timeout=300
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '').strip()
            else:
                raise Exception(f"LLM API returned status code {response.status_code}")
                
        except Exception as e:
            raise Exception(f"Error calling LLM: {e}")
    
    def verify_connection(self) -> bool:
        """Verify that the LLM service is accessible."""
        try:
            response = requests.get(f"{self.api_endpoint}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def _load_project_training_data(self, project_name: str, base_dir: str = "training_data") -> Dict[str, Any]:
        """
        Load training data for a specific project by name.
        
        Args:
            project_name: Name of the project
            base_dir: Base directory for all training data (default: "training_data")
            
        Returns:
            Dictionary containing training data for the project
        """
        base_path = Path(base_dir)
        project_data_file = base_path / project_name / "training_data.json"
        
        # Try to load existing data
        if project_data_file.exists():
            try:
                with open(project_data_file, 'r') as f:
                    data = json.load(f)
                    print(f"✓ Loaded training data for project '{project_name}'")
                    return data
            except Exception as e:
                print(f"⚠ Error loading training data for '{project_name}': {e}")
                print("Creating new training data...")
        
        # Create new training data structure
        print(f"Creating new training data for project '{project_name}'")
        training_data = self._create_empty_training_data(project_name)
        
        # Save it
        base_path.mkdir(exist_ok=True)
        (base_path / project_name).mkdir(exist_ok=True)
        
        try:
            with open(project_data_file, 'w') as f:
                json.dump(training_data, f, indent=2)
            print(f"✓ Created training data at {project_data_file}")
        except Exception as e:
            print(f"✗ Error saving training data: {e}")
        
        return training_data
    
    def _create_empty_training_data(self, project_name: str) -> Dict[str, Any]:
        """Create an empty training data structure."""
        return {
            "project_name": project_name,
            "created_at": None,
            "file_summaries": {},
            "code_patterns": [],
            "bug_examples": [],
            "optimization_examples": [],
            "review_history": [],
            "custom_rules": [],
            "metadata": {
                "total_files_analyzed": 0,
                "last_updated": None,
                "language_distribution": {}
            }
        }
    
    def save_project_training_data(self, base_dir: str = "training_data") -> bool:
        """
        Save the current training data to disk.
        
        Args:
            base_dir: Base directory for all training data (default: "training_data")
            
        Returns:
            True if successful, False otherwise
        """
        if not self.project_name or not self.training_data:
            print("✗ No project name or training data to save")
            return False
        
        base_path = Path(base_dir)
        project_data_file = base_path / self.project_name / "training_data.json"
        
        try:
            base_path.mkdir(exist_ok=True)
            (base_path / self.project_name).mkdir(exist_ok=True)
            with open(project_data_file, 'w') as f:
                json.dump(self.training_data, f, indent=2)
            print(f"✓ Saved training data for '{self.project_name}'")
            return True
        except Exception as e:
            print(f"✗ Error saving training data: {e}")
            return False
    
    def load_or_create_training_data(self, project_path: str, data_dir: str = "training_data") -> Dict[str, Any]:
        """
        Load existing training data for a project or create a new training data structure.
        
        Args:
            project_path: Path to the project directory
            data_dir: Directory name for training data (default: "training_data")
            
        Returns:
            Dictionary containing training data structure with metadata
        """
        project_path = Path(project_path).resolve()
        training_data_path = project_path / data_dir
        training_data_file = training_data_path / "training_data.json"
        
        # Create directory if it doesn't exist
        training_data_path.mkdir(exist_ok=True)
        
        # Try to load existing data
        if training_data_file.exists():
            try:
                with open(training_data_file, 'r') as f:
                    data = json.load(f)
                    print(f"✓ Loaded existing training data from {training_data_file}")
                    return data
            except Exception as e:
                print(f"⚠ Error loading training data: {e}")
                print("Creating new training data structure...")
        
        # Create new training data structure
        training_data = {
            "project_name": project_path.name,
            "project_path": str(project_path),
            "created_at": None,  # You can add timestamp if needed
            "file_summaries": {},
            "code_patterns": [],
            "bug_examples": [],
            "optimization_examples": [],
            "review_history": [],
            "custom_rules": [],
            "metadata": {
                "total_files_analyzed": 0,
                "last_updated": None,
                "language_distribution": {}
            }
        }
        
        # Save the new structure
        try:
            with open(training_data_file, 'w') as f:
                json.dump(training_data, f, indent=2)
            print(f"✓ Created new training data at {training_data_file}")
        except Exception as e:
            print(f"✗ Error saving training data: {e}")
        
        return training_data
    
    def save_training_data(self, project_path: str, data: Dict[str, Any], data_dir: str = "training_data") -> bool:
        """
        Save training data to disk.
        
        Args:
            project_path: Path to the project directory
            data: Training data dictionary to save
            data_dir: Directory name for training data (default: "training_data")
            
        Returns:
            True if successful, False otherwise
        """
        project_path = Path(project_path).resolve()
        training_data_path = project_path / data_dir
        training_data_file = training_data_path / "training_data.json"
        
        try:
            training_data_path.mkdir(exist_ok=True)
            with open(training_data_file, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"✗ Error saving training data: {e}")
            return False


class BugFinder(LLMAssistant):
    """Find and analyze potential bugs in code."""
    
    def __init__(self, project_name: Optional[str] = None, config: Optional[Config] = None):
        super().__init__(project_name, config)


class CodeReviewer(LLMAssistant):
    """Perform code reviews and provide suggestions."""
    
    def __init__(self, project_name: Optional[str] = None, config: Optional[Config] = None):
        super().__init__(project_name, config)


class CodeExplainer(LLMAssistant):
    """Explain code functionality and logic."""
    
    def __init__(self, project_name: Optional[str] = None, config: Optional[Config] = None):
        super().__init__(project_name, config)


class CodeOptimizer(LLMAssistant):
    """Suggest optimizations and improvements for code."""
    
    def __init__(self, project_name: Optional[str] = None, config: Optional[Config] = None):
        super().__init__(project_name, config)
