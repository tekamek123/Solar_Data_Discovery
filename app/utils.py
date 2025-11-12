"""
Utility functions for data processing and visualization in the Streamlit dashboard
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy.stats import f_oneway, kruskal

def get_data_path(filename):
    """
    Get the absolute path to a data file
    
    Args:
        filename: Name of the data file
    
    Returns:
        Absolute path to the data file
    """
    # Get the directory where this file is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level to project root
    project_root = os.path.dirname(current_dir)
    # Construct path to data file
    return os.path.join(project_root, 'data', filename)

def load_country_data(country_name):
    """
    Load cleaned dataset for a specific country
    
    Args:
        country_name: Name of the country ('Benin', 'Sierra Leone', or 'Togo')
    
    Returns:
        DataFrame with the country's data
    """
    country_files = {
        'Benin': 'benin_clean.csv',
        'Sierra Leone': 'sierraleone_clean.csv',
        'Togo': 'togo_clean.csv'
    }
    
    if country_name not in country_files:
        raise ValueError(f"Unknown country: {country_name}")
    
    file_path = get_data_path(country_files[country_name])
    df = pd.read_csv(file_path)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df.set_index('Timestamp', inplace=True)
    df['Country'] = country_name
    
    return df

def load_all_countries():
    """
    Load all three country datasets
    
    Returns:
        Combined DataFrame with all countries
    """
    benin = load_country_data('Benin')
    sierraleone = load_country_data('Sierra Leone')
    togo = load_country_data('Togo')
    
    all_data = pd.concat([benin, sierraleone, togo], ignore_index=False)
    return all_data

def calculate_summary_stats(df, metric='GHI'):
    """
    Calculate summary statistics for a given metric
    
    Args:
        df: DataFrame with country data
        metric: Metric to analyze (default: 'GHI')
    
    Returns:
        DataFrame with summary statistics by country
    """
    summary = df.groupby('Country')[metric].agg([
        'mean', 'median', 'std', 'min', 'max', 'count'
    ]).round(2)
    summary.columns = ['Mean', 'Median', 'Std Dev', 'Min', 'Max', 'Count']
    return summary

def perform_statistical_test(df, metric='GHI'):
    """
    Perform statistical tests (ANOVA and Kruskal-Wallis) on metric across countries
    
    Args:
        df: DataFrame with country data
        metric: Metric to test (default: 'GHI')
    
    Returns:
        Dictionary with test results
    """
    countries = df['Country'].unique()
    country_data = [df[df['Country'] == country][metric].dropna() for country in countries]
    
    # Kruskal-Wallis test (non-parametric)
    h_stat, p_kruskal = kruskal(*country_data)
    
    # ANOVA test
    f_stat, p_anova = f_oneway(*country_data)
    
    return {
        'kruskal_wallis': {
            'h_statistic': h_stat,
            'p_value': p_kruskal,
            'significant': p_kruskal < 0.05
        },
        'anova': {
            'f_statistic': f_stat,
            'p_value': p_anova,
            'significant': p_anova < 0.05
        }
    }

def create_comparison_boxplot(df, metric='GHI', countries=None):
    """
    Create a boxplot comparing a metric across countries
    
    Args:
        df: DataFrame with country data
        metric: Metric to plot
        countries: List of countries to include (None = all)
    
    Returns:
        matplotlib figure
    """
    if countries:
        df = df[df['Country'].isin(countries)]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=df, x='Country', y=metric, ax=ax, 
                palette=['#FF6B35', '#004E89', '#06A77D'])
    ax.set_title(f'{metric} Comparison Across Countries', fontsize=14, fontweight='bold')
    ax.set_xlabel('Country', fontsize=12)
    ax.set_ylabel(f'{metric} (W/m²)', fontsize=12)
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    return fig

def rank_countries_by_metric(df, metric='GHI'):
    """
    Rank countries by average value of a metric
    
    Args:
        df: DataFrame with country data
        metric: Metric to rank by
    
    Returns:
        DataFrame with countries ranked by metric
    """
    ranking = df.groupby('Country')[metric].mean().sort_values(ascending=False)
    ranking_df = pd.DataFrame({
        'Country': ranking.index,
        f'Average {metric}': ranking.values,
        'Rank': range(1, len(ranking) + 1)
    })
    return ranking_df

