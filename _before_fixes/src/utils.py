"""
Utility functions for the web scraper.
"""
import json
import csv
import re
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import pandas as pd


def save_to_json(data: Any, filename: str, output_dir: str = "data/processed") -> str:
    """Save data to JSON file.
    
    Args:
        data: Data to save
        filename: Output filename
        output_dir: Output directory path
        
    Returns:
        Absolute path to saved file
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    filepath = output_path / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    return str(filepath.absolute())


def save_to_csv(data: List[Dict], filename: str, output_dir: str = "data/processed") -> str:
    """Save data to CSV file.
    
    Args:
        data: List of dictionaries to save
        filename: Output filename
        output_dir: Output directory path
        
    Returns:
        Absolute path to saved file
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    filepath = output_path / filename
    
    if not data:
        # Create empty file
        open(filepath, 'w').close()
        return str(filepath.absolute())
    
    # Get all unique keys from all dictionaries
    keys = set()
    for item in data:
        keys.update(item.keys())
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=sorted(keys))
        writer.writeheader()
        writer.writerows(data)
    
    return str(filepath.absolute())


def save_to_excel(data: List[Dict], filename: str, output_dir: str = "data/processed", 
                  sheet_name: str = "Sheet1") -> str:
    """Save data to Excel file.
    
    Args:
        data: List of dictionaries to save
        filename: Output filename
        output_dir: Output directory path
        sheet_name: Name of the Excel sheet
        
    Returns:
        Absolute path to saved file
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    filepath = output_path / filename
    
    df = pd.DataFrame(data)
    df.to_excel(filepath, sheet_name=sheet_name, index=False)
    
    return str(filepath.absolute())


def clean_text(text: str) -> str:
    """Clean and normalize text.
    
    Args:
        text: Text to clean
        
    Returns:
        Cleaned text
    """
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Remove special characters if needed
    # text = re.sub(r'[^\w\s\-.,!?]', '', text)
    
    return text.strip()


def get_timestamp(format: str = "%Y%m%d_%H%M%S") -> str:
    """Get current timestamp as formatted string.
    
    Args:
        format: strftime format string
        
    Returns:
        Formatted timestamp
    """
    return datetime.now().strftime(format)
