"""
Test cases for the calculations module.
"""

import pytest
import pandas as pd
from src.calculations import LCACalculator

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'material': ['steel', 'aluminum', 'plastic'],
        'quantity': [100, 50, 75],
        'unit': ['kg', 'kg', 'kg'],
        'stage': ['manufacturing', 'manufacturing', 'manufacturing']
    })

@pytest.fixture
def calculator():
    return LCACalculator()

def test_calculate_impacts(calculator, sample_data):
    """Test impact calculations."""
    impacts = calculator.calculate_impacts(sample_data)
    
    # Check if all required columns are present
    assert all(col in impacts.columns for col in 
              ['material', 'quantity', 'unit', 'stage', 
               'carbon_impact', 'water_impact', 'energy_impact'])
    
    # Check if calculations are correct
    steel_row = impacts[impacts['material'] == 'steel'].iloc[0]
    assert steel_row['carbon_impact'] == 100 * calculator.impact_factors['carbon']['steel']
    assert steel_row['water_impact'] == 100 * calculator.impact_factors['water']['steel']
    assert steel_row['energy_impact'] == 100 * calculator.impact_factors['energy']['steel']

def test_normalize_impacts(calculator, sample_data):
    """Test impact normalization."""
    impacts = calculator.calculate_impacts(sample_data)
    normalized = calculator.normalize_impacts(impacts)
    
    # Check if all impact values are between 0 and 1
    for impact_type in ['carbon_impact', 'water_impact', 'energy_impact']:
        assert normalized[impact_type].max() <= 1
        assert normalized[impact_type].min() >= 0
    
    # Check if at least one value is 1 (maximum)
    assert any(normalized[impact_type].max() == 1 
              for impact_type in ['carbon_impact', 'water_impact', 'energy_impact']) 