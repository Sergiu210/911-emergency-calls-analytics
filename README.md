# 🚨 911 Emergency Calls Analytics Platform

End-to-end data engineering and analytics pipeline containerized with Docker. Ingests raw 911 emergency call logs into an indexed PostgreSQL database, serves aggregated metrics via a FastAPI REST API, and visualizes trends in an interactive Streamlit dashboard.

## 🏗️ Architecture

```text
[911.csv] ──▶ [ETL Container (Pandas/SQLAlchemy)] ──▶ [PostgreSQL 18 (Indexed)]
                                                              │
                                                              ▼
[Streamlit + Plotly Dashboard] ◀── HTTP/JSON ── [FastAPI Backend (/api/v1)]