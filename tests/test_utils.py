"""
Tests for utility functions.
"""
import pytest
import json
from pathlib import Path
from src.utils import (
    save_to_json,
    save_to_csv,
    save_to_excel,
    clean_text,
    get_timestamp,
    create_directories
)


def test_clean_text():
    """Test text cleaning."""
    # Test with extra whitespace
    text = "  This   has    extra   spaces  "
    cleaned = clean_text(text)
    assert cleaned == "This has extra spaces"
    
    # Test with empty string
    assert clean_text("") == ""
    
    # Test with None
    assert clean_text(None) == ""


def test_get_timestamp():
    """Test timestamp generation."""
    timestamp = get_timestamp()
    assert isinstance(timestamp, str)
    assert len(timestamp) == 15  # YYYYMMDD_HHMMSS format


def test_save_to_json(tmp_path):
    """Test saving data to JSON."""
    data = {"key": "value", "number": 42}
    filename = "test.json"
    
    filepath = save_to_json(data, filename, output_dir=str(tmp_path))
    
    assert Path(filepath).exists()
    with open(filepath, 'r') as f:
        loaded_data = json.load(f)
    assert loaded_data == data


def test_save_to_csv(tmp_path):
    """Test saving data to CSV."""
    data = [
        {"name": "Alice", "age": 30},
        {"name": "Bob", "age": 25}
    ]
    filename = "test.csv"
    
    filepath = save_to_csv(data, filename, output_dir=str(tmp_path))
    
    assert Path(filepath).exists()
    # Read and verify content
    import pandas as pd
    df = pd.read_csv(filepath)
    assert len(df) == 2
    assert list(df.columns) == ["name", "age"]


def test_save_to_excel(tmp_path):
    """Test saving data to Excel."""
    data = [
        {"product": "Widget", "price": 10.99},
        {"product": "Gadget", "price": 20.50}
    ]
    filename = "test.xlsx"
    
    filepath = save_to_excel(data, filename, output_dir=str(tmp_path))
    
    assert Path(filepath).exists()
    # Read and verify content
    import pandas as pd
    df = pd.read_excel(filepath)
    assert len(df) == 2
    assert list(df.columns) == ["product", "price"]


def test_save_to_csv_empty_data(tmp_path):
    """Test saving empty data to CSV."""
    data = []
    filename = "empty.csv"
    
    filepath = save_to_csv(data, filename, output_dir=str(tmp_path))
    assert Path(filepath).exists()


def test_create_directories(tmp_path):
    """Test directory creation."""
    # Change to tmp directory for testing
    import os
    original_dir = os.getcwd()
    os.chdir(tmp_path)
    
    try:
        create_directories()
        
        # Check if directories were created
        assert Path("data/raw").exists()
        assert Path("data/processed").exists()
        assert Path("logs").exists()
        assert Path("src").exists()
        assert Path("tests").exists()
        assert Path("examples").exists()
        
        # Check for .gitkeep files
        assert Path("data/raw/.gitkeep").exists()
        assert Path("data/processed/.gitkeep").exists()
    finally:
        os.chdir(original_dir)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
