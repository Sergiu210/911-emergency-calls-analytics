import os
import pandas as pd
from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:2703@127.0.0.1:5432/emergency_db")
engine = create_engine(DATABASE_URL)

# Verificăm dacă datele au fost deja importate
with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM emergency_calls")).scalar()

if result == 0:
    print("Se importă datele din 911.csv în PostgreSQL...")
    df = pd.read_csv('911.csv')
    df['timeStamp'] = pd.to_datetime(df['timeStamp'])

    df['category'] = df['title'].apply(lambda t: t.split(':')[0].strip() if ':' in str(t) else 'Unknown')
    df['call_subtype'] = df['title'].apply(lambda t: t.split(':')[1].strip() if ':' in str(t) else t)

    df = df.rename(columns={
        'zip': 'zip_code',
        'desc': 'description',
        'timeStamp': 'time_stamp',
        'twp': 'township',
        'addr': 'address'
    })
    if 'e' in df.columns:
        df = df.drop(columns=['e'])

    df.to_sql('emergency_calls', engine, if_exists='append', index=False, chunksize=5000)
    print("Import finalizat cu succes!")
else:
    print(f"Tabelul conține deja {result} înregistrări. Se sare peste import.")