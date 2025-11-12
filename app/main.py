"""
Streamlit Dashboard for Solar Data Discovery
Interactive visualization of solar farm data from Benin, Sierra Leone, and Togo
"""
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils import (
    load_country_data,
    load_all_countries,
    calculate_summary_stats,
    perform_statistical_test,
    create_comparison_boxplot,
    rank_countries_by_metric
)

# Page configuration
st.set_page_config(
    page_title="Solar Data Discovery Dashboard",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2c3e50;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #3498db;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and header
st.markdown('<h1 class="main-header">☀️ Solar Data Discovery Dashboard</h1>', unsafe_allow_html=True)
st.markdown("### Cross-Country Solar Potential Analysis for MoonLight Energy Solutions")

# Sidebar
st.sidebar.header("📊 Dashboard Controls")

# Country selection
st.sidebar.subheader("Country Selection")
selected_countries = st.sidebar.multiselect(
    "Select countries to compare:",
    ["Benin", "Sierra Leone", "Togo"],
    default=["Benin", "Sierra Leone", "Togo"]
)

# Metric selection
st.sidebar.subheader("Metric Selection")
selected_metric = st.sidebar.selectbox(
    "Select metric to analyze:",
    ["GHI", "DNI", "DHI", "Tamb", "RH", "WS"],
    index=0
)

# Load data
@st.cache_data
def load_data():
    """Load all country data (cached for performance)"""
    try:
        return load_all_countries()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

all_data = load_data()

if all_data is not None and len(selected_countries) > 0:
    # Filter data by selected countries
    filtered_data = all_data[all_data['Country'].isin(selected_countries)]
    
    # Main content area
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Total Records",
            f"{len(filtered_data):,}",
            help="Total number of data records across selected countries"
        )
    
    with col2:
        avg_metric = filtered_data[selected_metric].mean()
        st.metric(
            f"Average {selected_metric}",
            f"{avg_metric:.2f} W/m²" if selected_metric in ['GHI', 'DNI', 'DHI'] else f"{avg_metric:.2f}",
            help=f"Average {selected_metric} across selected countries"
        )
    
    with col3:
        countries_count = len(selected_countries)
        st.metric(
            "Countries Selected",
            countries_count,
            help="Number of countries included in analysis"
        )
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Visualizations", "📊 Summary Statistics", "🏆 Rankings", "🔬 Statistical Analysis"])
    
    with tab1:
        st.header("Visual Comparisons")
        
        # Boxplot comparison
        st.subheader(f"{selected_metric} Comparison - Boxplot")
        fig_box = create_comparison_boxplot(filtered_data, selected_metric, selected_countries)
        st.pyplot(fig_box)
        plt.close()
        
        # Additional visualizations
        col_viz1, col_viz2 = st.columns(2)
        
        with col_viz1:
            st.subheader("Time Series Overview")
            # Sample data for time series (daily averages)
            if len(filtered_data) > 0:
                daily_avg = filtered_data.groupby([filtered_data.index.date, 'Country'])[selected_metric].mean().reset_index()
                daily_avg['Date'] = pd.to_datetime(daily_avg['Timestamp'])
                
                fig_ts, ax = plt.subplots(figsize=(12, 6))
                for country in selected_countries:
                    country_data = daily_avg[daily_avg['Country'] == country]
                    ax.plot(country_data['Date'], country_data[selected_metric], 
                           label=country, linewidth=2, alpha=0.7)
                ax.set_xlabel('Date', fontsize=11)
                ax.set_ylabel(f'{selected_metric} (W/m²)' if selected_metric in ['GHI', 'DNI', 'DHI'] else selected_metric, fontsize=11)
                ax.set_title(f'{selected_metric} - Daily Average by Country', fontsize=12, fontweight='bold')
                ax.legend()
                ax.grid(True, alpha=0.3)
                plt.xticks(rotation=45)
                plt.tight_layout()
                st.pyplot(fig_ts)
                plt.close()
        
        with col_viz2:
            st.subheader("Distribution Histogram")
            fig_hist, ax = plt.subplots(figsize=(10, 6))
            for country in selected_countries:
                country_data = filtered_data[filtered_data['Country'] == country][selected_metric]
                ax.hist(country_data.dropna(), bins=50, alpha=0.6, label=country, edgecolor='black')
            ax.set_xlabel(f'{selected_metric} (W/m²)' if selected_metric in ['GHI', 'DNI', 'DHI'] else selected_metric, fontsize=11)
            ax.set_ylabel('Frequency', fontsize=11)
            ax.set_title(f'{selected_metric} Distribution by Country', fontsize=12, fontweight='bold')
            ax.legend()
            ax.grid(True, alpha=0.3, axis='y')
            plt.tight_layout()
            st.pyplot(fig_hist)
            plt.close()
    
    with tab2:
        st.header("Summary Statistics")
        
        # Summary table
        summary_stats = calculate_summary_stats(filtered_data, selected_metric)
        st.subheader(f"{selected_metric} Statistics by Country")
        st.dataframe(summary_stats, use_container_width=True)
        
        # Download button
        csv = summary_stats.to_csv(index=True)
        st.download_button(
            label="📥 Download Summary Statistics (CSV)",
            data=csv,
            file_name=f"{selected_metric}_summary_stats.csv",
            mime="text/csv"
        )
        
        # Key insights
        st.subheader("Key Insights")
        highest_mean = summary_stats['Mean'].idxmax()
        most_consistent = summary_stats['Std Dev'].idxmin()
        
        st.info(f"🏆 **Highest Average {selected_metric}**: {highest_mean} ({summary_stats.loc[highest_mean, 'Mean']:.2f})")
        st.info(f"📊 **Most Consistent {selected_metric}**: {most_consistent} (Std Dev: {summary_stats.loc[most_consistent, 'Std Dev']:.2f})")
    
    with tab3:
        st.header("Country Rankings")
        
        # Ranking by selected metric
        ranking_df = rank_countries_by_metric(filtered_data, selected_metric)
        st.subheader(f"Ranking by Average {selected_metric}")
        
        # Display ranking table
        st.dataframe(ranking_df, use_container_width=True, hide_index=True)
        
        # Visual ranking chart
        fig_rank, ax = plt.subplots(figsize=(10, 6))
        colors = ['#FF6B35' if c == 'Benin' else '#004E89' if c == 'Sierra Leone' else '#06A77D' 
                 for c in ranking_df['Country']]
        bars = ax.bar(ranking_df['Country'], ranking_df[f'Average {selected_metric}'], 
                     color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)
        
        # Add value labels
        for bar, value in zip(bars, ranking_df[f'Average {selected_metric}']):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{value:.2f}',
                   ha='center', va='bottom', fontweight='bold')
        
        # Add rank numbers
        for i, (country, value) in enumerate(zip(ranking_df['Country'], ranking_df[f'Average {selected_metric}'])):
            ax.text(i, value + max(ranking_df[f'Average {selected_metric}']) * 0.02,
                   f'#{i+1}', ha='center', va='bottom', fontsize=14, fontweight='bold', color='darkblue')
        
        ax.set_title(f'Country Ranking by Average {selected_metric}', fontsize=14, fontweight='bold')
        ax.set_xlabel('Country', fontsize=12)
        ax.set_ylabel(f'Average {selected_metric} (W/m²)' if selected_metric in ['GHI', 'DNI', 'DHI'] else f'Average {selected_metric}', fontsize=12)
        ax.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        st.pyplot(fig_rank)
        plt.close()
    
    with tab4:
        st.header("Statistical Analysis")
        
        if len(selected_countries) >= 2:
            # Perform statistical tests
            test_results = perform_statistical_test(filtered_data, selected_metric)
            
            st.subheader("Kruskal-Wallis Test (Non-parametric)")
            col_k1, col_k2 = st.columns(2)
            with col_k1:
                st.metric("H-statistic", f"{test_results['kruskal_wallis']['h_statistic']:.4f}")
            with col_k2:
                p_kruskal = test_results['kruskal_wallis']['p_value']
                sig_status = "✅ Significant" if test_results['kruskal_wallis']['significant'] else "❌ Not Significant"
                st.metric("P-value", f"{p_kruskal:.6f}", sig_status)
            
            st.subheader("One-way ANOVA Test")
            col_a1, col_a2 = st.columns(2)
            with col_a1:
                st.metric("F-statistic", f"{test_results['anova']['f_statistic']:.4f}")
            with col_a2:
                p_anova = test_results['anova']['p_value']
                sig_status = "✅ Significant" if test_results['anova']['significant'] else "❌ Not Significant"
                st.metric("P-value", f"{p_anova:.6f}", sig_status)
            
            # Interpretation
            st.subheader("Interpretation")
            if test_results['kruskal_wallis']['significant']:
                st.success("✅ **Statistically significant differences** exist between the selected countries (p < 0.05). The observed differences are meaningful and not due to chance.")
            else:
                st.warning("❌ **No statistically significant differences** detected between countries (p >= 0.05). While there may be visual differences, they are not statistically significant.")
            
            st.info("💡 **Note**: Kruskal-Wallis is preferred for non-normal distributions. Both tests help determine if differences between countries are statistically meaningful.")
        else:
            st.warning("⚠️ Please select at least 2 countries to perform statistical comparison.")
    
    # Footer
    st.markdown("---")
    st.markdown("### 📝 About This Dashboard")
    st.markdown("""
    This interactive dashboard provides comprehensive analysis of solar farm data from three West African countries.
    Use the sidebar controls to customize your analysis by selecting countries and metrics of interest.
    
    **Data Source**: Cleaned datasets from individual country EDA analyses  
    **Purpose**: Support strategic solar investment decisions for MoonLight Energy Solutions
    """)

else:
    st.warning("⚠️ Please select at least one country from the sidebar to view the analysis.")
    st.info("💡 Use the sidebar controls to select countries and metrics.")

