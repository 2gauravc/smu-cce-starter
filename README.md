## Installation Instructions

If you are new to Python, follow these steps in a terminal from the project folder.

1. Open a terminal in the repository folder.
2. Create a virtual environment so your project dependencies stay separate from other Python projects:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Start Jupyter Notebook:

```bash
jupyter notebook
```

5. Open one of the notebooks in the `notebooks/` folder and run the cells to explore the data.

If you are using VS Code or Codespaces, you can also open the notebook files directly and run them from there.

## Code Walkthrough

This repository is a beginner starter for a financial data app. It is organized around notebooks that collect data, clean it, and prepare it for analysis.

- `README.md` — project overview and course context.
- `lessons/` — step-by-step course material and guidance.
- `requirements.txt` — the Python packages this project needs, such as `yfinance`, `pandas`, and `streamlit`.
- `notebooks/` — the main analysis work happens here.

Important notebook files:

- `notebooks/filings.ipynb` — looks at company filings and financial information.
- `notebooks/news.ipynb` — gathers news or market-related data and helps explore trends.
- `notebooks/stock_price_ratings.ipynb` — pulls stock prices and rating data to compare performance.

How the application works from start to finish:

1. A user opens a notebook in Jupyter.
2. The notebook imports Python libraries and fetches financial data using APIs or package tools such as `yfinance`.
3. The data is loaded into a pandas table, cleaned, and organized.
4. Charts or summaries are created to help explain trends and insights.
5. The results can later be expanded into a Streamlit web app or a cloud-hosted dashboard.

This repo is the foundation for building a simple financial analytics application that turns raw data into usable insight.

 # Cloud Computing for Economics: Starter Repo 

  This repository contains the starter code and lesson materials for building a Python financial-data application and deploying it to AWS.

  Students will use GitHub Codespaces, Python, Jupyter notebooks, Streamlit, Git, and AWS CloudFormation.

  ## Learning outcomes

  By the end of the course, you will be able to:

   1.  Build and deploy an analytics application with a simple Front End / back-end (using AI)
   2.  Host and share the application on a cloud platform (e.g., AWS EC2 or similar) so that others can access it securely over the web
   3.  Integrate data sources and APIs into the app to enable interactive, real-time analytics
   4.  Apply cloud architecture best practices, ensuring the app demonstrates scalability, performance efficiency, and basic security
   5.  Showcase your work on GitHub as part of a personal portfolio, demonstrating practical cloud and analytics skills through a shareable, explorable repository

  
  ## Repository structure

  ```text
  .
  ├── lessons/          # Step-by-step course instructions
  ├── notebooks/        # Starter financial-data notebooks
  ├── requirements.txt  # Python dependencies
  └── README.md         # Course overview