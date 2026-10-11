# Trading Demo App

This is a paper-trading FastAPI application with a TradingView-inspired NSE dashboard. It creates a local SQLite database, seeds Indian stock symbols on first start, and includes searchable watchlists, canvas price charts, OHLC timeline data, holdings, orders, and paper-fund flows. No live exchange data or real bank payments are used.

## Run

Create a virtual environment, install the requirements, and run from `project_trade`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/app` for the trading UI and `http://127.0.0.1:8000/docs` for the API. The normal demo flow is register, login, link an account, deposit paper cash, search/select an Indian stock, inspect the chart/timeline, then buy or sell.

For production, replace the demo JWT secret and point `DATABASE_URL` at PostgreSQL, use migrations, a payment-provider integration, market-data feed, CSRF/rate-limit controls, and an audited exchange-order workflow.
