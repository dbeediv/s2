# ML functions here
import pandas as pd
from datetime import datetime
import sqlite3
import random

def get_inventory(conn: sqlite3.Connection) -> pd.DataFrame:
    df = pd.read_sql_query("SELECT * FROM inventory", conn)
    return df

def predict_spoilage(df: pd.DataFrame) -> pd.DataFrame:
    """
    Simple heuristic spoilage risk: days to expiry mapped to 0-1
    """
    today = datetime.today()
    risks = []
    for _, row in df.iterrows():
        try:
            expiry = datetime.strptime(row['expiry_date'], "%Y-%m-%d")
            days_left = (expiry - today).days
            risk = max(0, min(1, 1 - days_left/30))  # 0=no risk, 1=high risk
        except:
            risk = random.random()  # fallback
        risks.append(risk)
    df['spoilage_risk'] = risks
    return df
