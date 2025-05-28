"""
Calculations module for LCA tool.
Handles environmental impact calculations and analysis.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Union

class LCACalculator:
    def __init__(self):
        # Example impact factors (these should be replaced with real data)
        self.impact_factors = {
            'carbon': {
                'steel': 1.8,  # kg CO2e per kg
                'aluminum': 8.1,
                'plastic': 2.7,
                'paper': 0.9,
            },
            'water': {
                'steel': 300,  # liters per kg
                'aluminum': 1500,
                'plastic': 200,
                'paper': 100,
            },
            'energy': {
                'steel': 20,  # MJ per kg
                'aluminum': 150,
                'plastic': 80,
                'paper': 15,
            }
        }
    
    def calculate_impacts(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate environmental impacts for each material.
        
        Args:
            data: DataFrame containing material quantities
            
        Returns:
            DataFrame with calculated impacts
        """
        results = []
        
        for _, row in data.iterrows():
            material = row['material'].lower()
            quantity = row['quantity']
            
            impacts = {
                'material': material,
                'quantity': quantity,
                'unit': row['unit'],
                'stage': row['stage'],
                'carbon_impact': quantity * self.impact_factors['carbon'].get(material, 0),
                'water_impact': quantity * self.impact_factors['water'].get(material, 0),
                'energy_impact': quantity * self.impact_factors['energy'].get(material, 0)
            }
            results.append(impacts)
            
        return pd.DataFrame(results)
    
    def normalize_impacts(self, impacts: pd.DataFrame) -> pd.DataFrame:
        """
        Normalize impacts to a common scale (0-1).
        
        Args:
            impacts: DataFrame with calculated impacts
            
        Returns:
            DataFrame with normalized impacts
        """
        normalized = impacts.copy()
        
        for impact_type in ['carbon_impact', 'water_impact', 'energy_impact']:
            max_value = impacts[impact_type].max()
            if max_value > 0:
                normalized[impact_type] = impacts[impact_type] / max_value
                
        return normalized 