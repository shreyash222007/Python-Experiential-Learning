# Personal Expense Tracker — Web App

A browser-based version of the Python Personal Expense Tracker using Streamlit, SQLite, Pandas, and Matplotlib.

## Features
- Add expenses with date, amount, category, and description
- View all expenses and total spending
- Category-wise summary and bar chart
- Search expenses by category
- Delete an expense
- Monthly report with bar and pie charts
- SQLite database for storing records between local runs

## Run locally
1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Start the web app:

   ```bash
   python -m streamlit run app.py
   ```

5. Your browser should open automatically. If not, visit `http://localhost:8501`.

## Deploy with Streamlit Community Cloud
1. Create a GitHub repository and upload `app.py` and `requirements.txt`.
2. Sign in to Streamlit Community Cloud with GitHub.
3. Create a new app and select your repository, branch, and `app.py`.
4. Click Deploy.

## Important database note
The SQLite database is convenient for a local project demo. On hosted services, a local file may not be permanent across restarts/redeployments. For long-term multi-user use, connect a managed database such as PostgreSQL or another persistent database service. This demo is intended as a student project, not a production financial service.
