# NSE Trading Demo

This is a paper-trading FastAPI application. It creates a local SQLite database and seeds ten NSE symbols on first start. No live exchange data or real bank payments are used.

## Run

Create a virtual environment, install the requirements, and run from `project_trade`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/app` for the test UI and `http://127.0.0.1:8000/docs` for the API. The normal demo flow is register, login, link an account, deposit paper cash, then buy or sell.

For production, replace the demo JWT secret and point `DATABASE_URL` at PostgreSQL, use migrations, a payment-provider integration, market-data feed, CSRF/rate-limit controls, and an audited exchange-order workflow.
