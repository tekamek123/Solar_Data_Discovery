# Solar Challenge Week 1

## Project Overview

This project analyzes solar farm data from three locations (Benin, Sierra Leone, and Togo) to identify high-potential regions for solar installation. The analysis supports MoonLight Energy Solutions' strategic approach to enhance operational efficiency and sustainability through targeted solar investments.

## Repository Structure

```
├── .vscode/
│   └── settings.json
├── .github/
│   └── workflows/
│       └── ci.yml
├── .gitignore
├── requirements.txt
├── README.md
├── src/
├── notebooks/
│   ├── __init__.py
│   └── README.md
├── tests/
│   ├── __init__.py
└── scripts/
    ├── __init__.py
    └── README.md
```

## Environment Setup

### Prerequisites

- Python 3.8 or higher
- Git
- (Optional) Conda or Miniconda

### Setup Instructions

#### Option 1: Using venv (Recommended)

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd solar-challenge-week1
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. **Verify installation**:
   ```bash
   python --version
   pip list
   ```

#### Option 2: Using Conda

1. **Create a conda environment**:
   ```bash
   conda create -n solar-challenge python=3.10
   conda activate solar-challenge
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Running Jupyter Notebooks

1. **Activate your virtual environment** (if not already active)

2. **Start Jupyter Notebook**:
   ```bash
   jupyter notebook
   ```

3. **Or use JupyterLab**:
   ```bash
   jupyter lab
   ```

## Data

The dataset contains solar radiation and weather measurements from three locations:
- Benin (Malanville)
- Sierra Leone (Bumbuna)
- Togo (Dapaong)

**Note**: Data files are excluded from the repository via `.gitignore`. Ensure you have access to the data files locally in the `data/` directory.

## Development Workflow

1. Create a new branch for your work:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and commit:
   ```bash
   git add .
   git commit -m "feat: your commit message"
   ```

3. Push and create a Pull Request:
   ```bash
   git push origin feature/your-feature-name
   ```

## CI/CD

This repository uses GitHub Actions for continuous integration. The workflow automatically:
- Runs on push and pull requests
- Verifies Python version
- Installs dependencies from `requirements.txt`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is part of the Kifiya AI Mastery Training program.

