"""
Data input module for LCA tool.
Handles reading and validating input data from various sources.
"""

import pandas as pd
import json
from pathlib import Path
from typing import Dict, List, Union

class DataInput:
    def __init__(self):
        self.supported_formats = ['.csv', '.xlsx', '.json']
    
    def read_data(self, file_path: Union[str, Path]) -> pd.DataFrame:
        """
        Read data from various file formats.
        
        Args:
            file_path: Path to the input file
            
        Returns:
            DataFrame containing the input data
            
        Raises:
            ValueError: If file format is not supported
            FileNotFoundError: If file does not exist
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
            
        if file_path.suffix not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")
            
        if file_path.suffix == '.csv':
            return pd.read_csv(file_path)
        elif file_path.suffix == '.xlsx':
            return pd.read_excel(file_path)
        elif file_path.suffix == '.json':
            return pd.read_json(file_path)
            
    def validate_data(self, data: pd.DataFrame) -> bool:
        """
        Validate input data structure and content.
        
        Args:
            data: DataFrame to validate
            
        Returns:
            bool: True if data is valid, False otherwise
        """
        required_columns = ['material', 'quantity', 'unit', 'stage']
        return all(col in data.columns for col in required_columns) 