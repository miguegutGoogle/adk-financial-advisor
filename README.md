# Financial Advisor Agent (ADK)

This repository contains a multi-agent financial analysis system built using the **Google Agent Development Kit (ADK)**. It features a lead "Pro Advisor" agent and a specialized "Data Analyst" sub-agent that fetches real-time market data using `yfinance`.

## 🚀 Features

* **Multi-Agent Orchestration:** Uses a lead advisor to coordinate tasks and a sub-agent for data retrieval.
* **Real-time Data:** Integrated with `yfinance` to pull live market prices and company summaries.
* **Safety Callbacks:**
  * **Legal Disclaimer:** Automatically displays a financial warning before starting.
  * **Tool Filtering:** Blocks the analysis of specific cryptocurrencies (BTC, ETH, DOGE) at the tool level.
* **Performance Optimization:** Includes a demonstration of a cache callback for instant responses on specific tickers (e.g., GOOGL).

---

## 🛠️ Setup Instructions

Follow these steps to get the agent running on your local machine.

### 1. Create a Python Virtual Environment

It is highly recommended to use a virtual environment to manage dependencies and avoid conflicts.

```bash
# Create the environment
python3 -m venv pythonenv

# Activate the environment
# On macOS/Linux:
source pythonenv/bin/activate

# On Windows:
.\pythonenv\Scripts\activate
```

### 2. Install Dependencies

Once your virtual environment is activated, install the required libraries (including the Google ADK and `yfinance`).

```bash
pip install -r repo/requirements.txt
```
*(Note: Replace `repo/` with your actual repository directory name if different).*

---

## 🏃 How to Run

To run the agent using the ADK web interface, you must execute the command from the **parent directory** (the directory containing the repo folder).

**Directory Structure Reference:**

```text
parent_directory/  <-- RUN THE COMMAND FROM HERE
└── repo/
    ├── agent.py
    ├── requirements.txt
    └── __init__.py
```

**Launch Command:**

From your terminal in the parent directory, run:

```bash
adk web
```

Once the development server starts, open your browser to the provided local URL (usually `http://localhost:8080`) to interact with your Financial Advisor agent.

---

## 📝 Usage Note

The agent follows a strict workflow:

1. **Disclaimer:** You will see a legal warning first.
2. **Request:** Provide a stock ticker (e.g., "AAPL" or "MSFT").
3. **Analysis:** The `pro_advisor` will task the `data_analyst` to fetch data and then present a summary to you.
