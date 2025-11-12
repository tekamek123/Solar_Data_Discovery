# Streamlit Dashboard - Solar Data Discovery

## Overview
This interactive Streamlit dashboard provides comprehensive visualization and analysis of solar farm data from Benin, Sierra Leone, and Togo. The dashboard enables users to compare solar potential across countries, explore statistical relationships, and generate insights to support strategic investment decisions.

## Features

### Interactive Controls
- **Country Selection**: Choose one or more countries to compare (Benin, Sierra Leone, Togo)
- **Metric Selection**: Analyze different metrics including:
  - GHI (Global Horizontal Irradiance)
  - DNI (Direct Normal Irradiance)
  - DHI (Diffuse Horizontal Irradiance)
  - Tamb (Ambient Temperature)
  - RH (Relative Humidity)
  - WS (Wind Speed)

### Dashboard Tabs

1. **📈 Visualizations**
   - Boxplot comparisons across countries
   - Time series analysis (daily averages)
   - Distribution histograms

2. **📊 Summary Statistics**
   - Mean, median, standard deviation
   - Min/max values
   - Record counts
   - Downloadable CSV export

3. **🏆 Rankings**
   - Country rankings by metric
   - Visual bar charts with ranking indicators
   - Key insights on top performers

4. **🔬 Statistical Analysis**
   - Kruskal-Wallis test (non-parametric)
   - One-way ANOVA test
   - P-value interpretation
   - Significance testing results

## Installation

1. Ensure you have Python 3.8+ installed
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Verify the data files exist:
   - `data/benin_clean.csv`
   - `data/sierraleone_clean.csv`
   - `data/togo_clean.csv`

## Running the Dashboard

### Local Development
```bash
streamlit run app/main.py
```

The dashboard will open in your default web browser at `http://localhost:8501`

### Deployment to Streamlit Community Cloud

1. **Push your code to GitHub** (ensure `data/` folder is in `.gitignore`)

2. **Go to [Streamlit Community Cloud](https://share.streamlit.io/)**

3. **Sign in with GitHub** and click "New app"

4. **Configure your app**:
   - Repository: Select your GitHub repository
   - Branch: `dashboard-dev` (or `main` if merged)
   - Main file path: `app/main.py`

5. **Deploy**: Click "Deploy!" and wait for the app to build

6. **Access**: Your dashboard will be available at a public URL like:
   ```
   https://your-username-streamlit-app-xxx.streamlit.app
   ```

## Project Structure

```
├── app/
│   ├── __init__.py
│   ├── main.py          # Main Streamlit application
│   └── utils.py         # Utility functions for data processing
├── data/
│   ├── benin_clean.csv
│   ├── sierraleone_clean.csv
│   └── togo_clean.csv
├── requirements.txt
└── README_DASHBOARD.md
```

## Usage Instructions

1. **Select Countries**: Use the sidebar to choose which countries to analyze
2. **Choose Metric**: Select the metric you want to explore
3. **Explore Tabs**: Navigate through different analysis views
4. **Download Data**: Export summary statistics as CSV from the Summary Statistics tab
5. **Interpret Results**: Review statistical test results to understand significance

## Key Features

- ✅ Interactive country and metric selection
- ✅ Real-time visualization updates
- ✅ Statistical testing with interpretation
- ✅ Data export capabilities
- ✅ Responsive design
- ✅ Cached data loading for performance

## Development Process

This dashboard was developed as part of Task 3 (Bonus) of the Solar Data Discovery challenge:

1. Created `dashboard-dev` branch
2. Implemented modular architecture (`app/main.py`, `app/utils.py`)
3. Added interactive Streamlit widgets
4. Integrated statistical analysis functions
5. Designed clean, professional UI

## Git Workflow

```bash
# Create branch
git checkout -b dashboard-dev

# Commit changes
git add app/ requirements.txt README_DASHBOARD.md
git commit -m "feat: basic Streamlit UI with interactive elements"

# Push to remote
git push origin dashboard-dev

# Create Pull Request to merge into main
```

## Notes

- Data files (`data/*.csv`) are excluded from Git (in `.gitignore`)
- The dashboard reads data from local CSV files
- For deployment, ensure data files are available or modify to read from a remote source
- All visualizations are generated dynamically based on user selections

## Troubleshooting

### Import Errors
If you encounter import errors, ensure you're running from the project root directory:
```bash
cd "D:\My Projects\Kifiya AI Mastery Training"
streamlit run app/main.py
```

### Data Not Found
Verify that cleaned CSV files exist in the `data/` directory. If not, run the EDA notebooks first to generate them.

### Port Already in Use
If port 8501 is busy, Streamlit will automatically use the next available port. Check the terminal output for the actual URL.

## Future Enhancements

- [ ] Add date range filtering
- [ ] Implement seasonal analysis
- [ ] Add correlation heatmaps
- [ ] Include weather pattern analysis
- [ ] Export visualizations as images
- [ ] Add data refresh functionality

## Support

For issues or questions, refer to the main project README.md or CONTRIBUTIONS.md files.

