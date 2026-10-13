## Installation Instructions  

If you are new to Python, follow these steps in a terminal from the project folder.

1. Open a terminal in the repository folder.
2. Create a virtual environment so your project dependencies stay separate from other Python projects:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Run the Streamlit app:

```bash
python3 -m streamlit run src/app.py
```

4. Enter a stock ticker, choose an analysis type, and click Run.

If you are using VS Code or Codespaces, you can also open the notebook files directly and run them from there.

## Streamlit App

This project includes a beginner-friendly Streamlit interface in `src/app.py`.

- `src/app.py` contains the user interface and button logic
- `src/analysis.py` contains the reusable finance helper functions extracted from the notebooks

The app supports:

- filings analysis
- news analysis
- stock price ratings analysis
- saving an analysis as a Markdown file and viewing saved analyses

### Saving and viewing previous analyses

After running an analysis, select **Save Analysis** to write it as a Markdown
file. Saved analyses include the ticker, analysis type, selected parameters,
creation date, and results. Use **Previous Analyses** on the homepage to browse
saved files (newest first). Select an analysis and click **Show** to open it in
a pop-up; selecting it from the dropdown alone does not display its contents.

The app creates an `analyses-data/` folder at the project root when needed.
Its location is resolved from the app code, so the same commands and storage
behavior work in GitHub Codespaces and on EC2:

```bash
python3 -m streamlit run src/app.py
```

To verify the feature in either environment:

1. Run the command above and create an analysis, for example for `AAPL`.
2. Select **Save Analysis** and confirm the success message.
3. Confirm a `.md` file appears in `analyses-data/` at the project root. This
   folder is intentionally excluded from Git.
4. Refresh or rerun the app, select the saved analysis in **Previous
   Analyses**, and click **Show** to view it in a pop-up.

Each environment stores files on its existing project filesystem; files saved
in Codespaces are not automatically copied to EC2, and vice versa. EC2 uses
the instance's existing disk—no additional volume or CloudFormation changes
are required.

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