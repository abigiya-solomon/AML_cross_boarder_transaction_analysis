# transactions.py
from fastapi import FastAPI, Query
from app.db.database import get_db_session  # adapt to a function that returns a DB connection

app = FastAPI()

@app.get("/")
def list_transactions(skip: int = 0, limit: int = 50, search: str | None = None):
    db = get_db_session()
    # call into your existing get_transactions_list(db, ...) service
    result = get_transactions_list(db=db, skip=skip, limit=limit, search=search)
    return result