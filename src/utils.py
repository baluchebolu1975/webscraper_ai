"""
Utility functions for the web scraper.
"""
import json
import csv
import time
from pathlib import Path
from typing import Any, Optional
from datetime import datetime
import pandas as pd

# Constants
DEFAULT_OUTPUT_DIR = "data/processed"


def save_to_json(data: Any, filename: str, output_dir: str = DEFAULT_OUTPUT_DIR) -> str:
    """Save data to JSON file.
    
    Args:
        data: Data to save
        filename: Output filename
        output_dir: Output directory path
        
    Returns:
        Absolute path to saved file
        
    Raises:
        ValueError: If filename or output_dir contain path traversal attempts
    """
    # Security: Prevent path traversal
    filename = Path(filename).name  # Strip any directory components
    output_path = Path(output_dir).resolve()
    
    # Ensure output directory is within project root
    try:
        output_path.relative_to(Path.cwd())
    except ValueError:
        raise ValueError(f"Output directory must be within project root: {output_dir}")
    
    output_path.mkdir(parents=True, exist_ok=True)
    
    filepath = output_path / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    return str(filepath)


def save_to_csv(data: list[dict], filename: str, output_dir: str = DEFAULT_OUTPUT_DIR) -> str:
    """Save data to CSV file.
    
    Args:
        data: List of dictionaries to save
        filename: Output filename
        output_dir: Output directory path
        
    Returns:
        Absolute path to saved file
        
    Raises:
        ValueError: If filename contains path traversal attempts
    """
    # Security: Prevent path traversal
    filename = Path(filename).name
    output_path = Path(output_dir).resolve()
    
    try:
        output_path.relative_to(Path.cwd())
    except ValueError:
        raise ValueError(f"Output directory must be within project root: {output_dir}")
    
    output_path.mkdir(parents=True, exist_ok=True)
    
    filepath = output_path / filename
    
    if data:
        df = pd.DataFrame(data)
        df.to_csv(filepath, index=False, encoding='utf-8')
    
    return str(filepath)


def save_to_excel(data: list[dict], filename: str, output_dir: str = DEFAULT_OUTPUT_DIR) -> str:
    """Save data to Excel file.
    
    Args:
        data: List of dictionaries to save
        filename: Output filename
        output_dir: Output directory path
        
    Returns:
        Absolute path to saved file
        
    Raises:
        ValueError: If filename contains path traversal attempts
    """
    # Security: Prevent path traversal
    filename = Path(filename).name
    output_path = Path(output_dir).resolve()
    
    try:
        output_path.relative_to(Path.cwd())
    except ValueError:
        raise ValueError(f"Output directory must be within project root: {output_dir}")
    
    output_path.mkdir(parents=True, exist_ok=True)
    
    filepath = output_path / filename
    
    if data:
        df = pd.DataFrame(data)
        df.to_excel(filepath, index=False, engine='openpyxl')
    
    return str(filepath)


def clean_text(text: Optional[str]) -> str:
    """Clean and normalize text.
    
    Args:
        text: Text to clean
        
    Returns:
        Cleaned text with normalized whitespace
    """
    if not text:
        return ""
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text.strip()


def get_timestamp() -> str:
    """Get current timestamp as string."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def rate_limit(delay: float = 1.0):
    """Decorator to add rate limiting to functions."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            time.sleep(delay)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def create_directories():
    """Create necessary project directories."""
    directories = [
        "data/raw",
        "data/processed",
        "logs",
        "src",
        "tests",
        "examples"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        
        # Create .gitkeep files for empty directories
        gitkeep = Path(directory) / ".gitkeep"
        if not gitkeep.exists():
            gitkeep.touch()
