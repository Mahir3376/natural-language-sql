# Database Query Explorer

Turn plain English questions into SQL queries and visualizations for MySQL databases.

A **Streamlit-based tool** for exploring **MySQL databases** with support for:
- Schema browsing
- Custom SQL queries
- Quick visualizations
- Database statistics
- Natural Language Querying (NLQ) using LLMs (Groq)

---

## Features

- **Authentication**
  - Connect to any MySQL server with username + password.

- **Table Explorer**
  - Browse tables, view schema details, and fetch rows.

- **Custom SQL Query**
  - Run ad-hoc queries and preview/download results.

- **Visualization**
  - Quickly generate scatter plots from table data.

- **Database Info**
  - View per-table row counts and column counts.

- **Natural Language Queries**
  - Ask questions in plain English and get SQL + results (via Groq LLaMA).

---

## Installation

# 1) Clone the repo
 ```bash
git clone https://github.com/Mahir3376/natural-language-sql.git
```
# 2) Create and activate a virtual environment
 ```bash
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
```
# 3) Install dependencies
 ```bash
pip install -r requirements.txt
```
# 4) Start the Streamlit app
 ```bash
streamlit run src/app.py
```
## Configuration

- **Database Connection**
  - Enter your MySQL host, port, username, and password in the UI.  
  - Example defaults: `127.0.0.1`, port `3306`, user `NLQ_User`.

- **Natural Language Queries (NLQ)**
  - Requires a **Groq API key**.  
  - Set it as an environment variable before launching:  

    ```bash
    export GROQ_API_KEY="your_api_key_here"   # macOS/Linux
    setx GROQ_API_KEY "your_api_key_here"     # Windows
    ```

  - NLQ is powered by Groq LLaMA models for SQL generation. If no key is set, you can still use schema browsing, queries, and visualizations.

---

## Sample Questions You Can Ask

- *"What are the names of hotels in Hyderabad"*
- *"List all customers planning to go Hyderabad"*
- *"How many rooms are occupied overall in Bangalore Hotels?"*

---

## Requirements

See `requirements.txt` for dependencies.

---

## License

MIT License © 2025

---
