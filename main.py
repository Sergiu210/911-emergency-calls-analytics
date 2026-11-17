import os
from typing import Optional
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text
import uvicorn

app = FastAPI(title="911 Emergency Calls API")

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:2703@127.0.0.1:5432/emergency_db")
engine = create_engine(DATABASE_URL)


@app.get("/api/v1/calls/by-category")
def get_calls_by_category():
    query = text("""
        SELECT category, COUNT(*) AS count
        FROM emergency_calls
        GROUP BY category
        ORDER BY count DESC
    """)
    try:
        with engine.connect() as conn:
            result = conn.execute(query).mappings().all()
            return [dict(row) for row in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Eroare bază de date: {e}")


@app.get("/api/v1/calls/monthly-trends")
def get_monthly_trends():
    query = text("""
        SELECT 
            EXTRACT(MONTH FROM time_stamp)::int AS month,
            category,
            COUNT(*) AS count
        FROM emergency_calls
        WHERE time_stamp IS NOT NULL
        GROUP BY month, category
        ORDER BY month ASC, category ASC
    """)
    try:
        with engine.connect() as conn:
            result = conn.execute(query).mappings().all()
            return [dict(row) for row in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Eroare bază de date: {e}")


@app.get("/api/v1/metrics/summary")
def get_metrics_summary():
    query = text("""
        SELECT 
            COUNT(*) AS total_calls,
            COUNT(DISTINCT township) AS total_townships,
            COUNT(DISTINCT zip_code) AS total_zipcodes
        FROM emergency_calls
    """)
    try:
        with engine.connect() as conn:
            row = conn.execute(query).mappings().first()
            return dict(row) if row else {"total_calls": 0, "total_townships": 0, "total_zipcodes": 0}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Eroare bază de date: {e}")


@app.get("/api/v1/calls/download")
def download_calls(category: Optional[str] = None):
    try:
        with engine.connect() as conn:
            if category:
                query = text("""
                    SELECT lat, lng, description, zip_code, title, category, call_subtype, time_stamp, township, address
                    FROM emergency_calls
                    WHERE category = :category
                """)
                result = conn.execute(query, {"category": category}).mappings().all()
            else:
                query = text("""
                    SELECT lat, lng, description, zip_code, title, category, call_subtype, time_stamp, township, address
                    FROM emergency_calls
                """)
                result = conn.execute(query).mappings().all()
            return [dict(row) for row in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Eroare bază de date: {e}")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)