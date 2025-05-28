"""
Utilities module for LCA tool.
Contains helper functions and constants.
"""

import pandas as pd
from typing import Dict, List, Union
from pathlib import Path

# Unit conversion factors
UNIT_CONVERSIONS = {
    'kg': {
        'g': 1000,
        'ton': 0.001,
        'lb': 2.20462
    },
    'L': {
        'mL': 1000,
        'm3': 0.001,
        'gal': 0.264172
    },
    'MJ': {
        'kJ': 1000,
        'kWh': 0.277778,
        'BTU': 947.817
    }
}

def convert_units(value: float, from_unit: str, to_unit: str) -> float:
    """
    Convert values between different units.
    
    Args:
        value: Value to convert
        from_unit: Source unit
        to_unit: Target unit
        
    Returns:
        Converted value
        
    Raises:
        ValueError: If units are not supported
    """
    # Find the base unit for the conversion
    base_unit = None
    for base, conversions in UNIT_CONVERSIONS.items():
        if from_unit in conversions or to_unit in conversions:
            base_unit = base
            break
    
    if not base_unit:
        raise ValueError(f"Unsupported units: {from_unit} or {to_unit}")
    
    # Convert to base unit
    if from_unit != base_unit:
        value = value / UNIT_CONVERSIONS[base_unit][from_unit]
    
    # Convert from base unit to target unit
    if to_unit != base_unit:
        value = value * UNIT_CONVERSIONS[base_unit][to_unit]
    
    return value

def save_results(data: pd.DataFrame, file_path: Union[str, Path], 
                format: str = 'csv') -> None:
    """
    Save analysis results to file.
    
    Args:
        data: DataFrame to save
        file_path: Path to save file
        format: File format ('csv', 'xlsx', or 'json')
        
    Raises:
        ValueError: If format is not supported
    """
    file_path = Path(file_path)
    
    if format == 'csv':
        data.to_csv(file_path, index=False)
    elif format == 'xlsx':
        data.to_excel(file_path, index=False)
    elif format == 'json':
        data.to_json(file_path, orient='records')
    else:
        raise ValueError(f"Unsupported format: {format}")

def load_impact_factors(file_path: Union[str, Path]) -> Dict:
    """
    Load impact factors from a JSON file.
    
    Args:
        file_path: Path to impact factors file
        
    Returns:
        Dictionary of impact factors
        
    Raises:
        FileNotFoundError: If file does not exist
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"Impact factors file not found: {file_path}")
    
    with open(file_path, 'r') as f:
        return pd.read_json(f).to_dict() 