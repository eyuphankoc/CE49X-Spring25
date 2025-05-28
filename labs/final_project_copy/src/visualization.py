"""
Visualization module for LCA tool.
Handles creation of plots and charts for impact analysis.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Optional

class LCAVisualizer:
    def __init__(self):
        plt.style.use('seaborn')
        self.colors = sns.color_palette("husl", 8)
    
    def plot_impact_breakdown(self, data: pd.DataFrame, impact_type: str, 
                            title: Optional[str] = None) -> plt.Figure:
        """
        Create a pie chart showing impact breakdown by material.
        
        Args:
            data: DataFrame with impact data
            impact_type: Type of impact to plot (e.g., 'carbon_impact')
            title: Optional title for the plot
            
        Returns:
            matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        impact_data = data.groupby('material')[impact_type].sum()
        ax.pie(impact_data, labels=impact_data.index, autopct='%1.1f%%',
               colors=self.colors[:len(impact_data)])
        
        if title:
            ax.set_title(title)
        else:
            ax.set_title(f'{impact_type.replace("_", " ").title()} by Material')
            
        return fig
    
    def plot_stage_comparison(self, data: pd.DataFrame, 
                            impact_types: List[str]) -> plt.Figure:
        """
        Create a bar chart comparing impacts across life cycle stages.
        
        Args:
            data: DataFrame with impact data
            impact_types: List of impact types to compare
            
        Returns:
            matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        stage_data = data.groupby('stage')[impact_types].sum()
        stage_data.plot(kind='bar', ax=ax)
        
        ax.set_title('Impact Comparison Across Life Cycle Stages')
        ax.set_xlabel('Life Cycle Stage')
        ax.set_ylabel('Impact')
        plt.xticks(rotation=45)
        plt.legend(title='Impact Type')
        
        return fig
    
    def plot_trend_analysis(self, data: pd.DataFrame, impact_type: str,
                          time_column: str) -> plt.Figure:
        """
        Create a line plot showing impact trends over time.
        
        Args:
            data: DataFrame with impact data
            impact_type: Type of impact to plot
            time_column: Column containing time data
            
        Returns:
            matplotlib Figure object
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        
        for material in data['material'].unique():
            material_data = data[data['material'] == material]
            ax.plot(material_data[time_column], material_data[impact_type],
                   label=material, marker='o')
        
        ax.set_title(f'{impact_type.replace("_", " ").title()} Trends')
        ax.set_xlabel('Time')
        ax.set_ylabel('Impact')
        plt.legend()
        
        return fig 