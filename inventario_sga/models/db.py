import pyodbc
import os
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

def get_connection():
    try:
        conn = pyodbc.connect(
            f"DRIVER={{{os.getenv('DB_DRIVER')}}};"
            f"SERVER={os.getenv('DB_SERVER')};"
            f"DATABASE={os.getenv('DB_NAME')};"
            "Trusted_Connection=yes;"
        )
        return conn
    except Exception as e:
        print("Error conectando a SQL Server:", e)
        return None
