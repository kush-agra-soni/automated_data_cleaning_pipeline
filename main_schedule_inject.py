# core/scheduled_inject_method.py

import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor
from utils.logger import get_logger

logger = get_logger("scheduled_inject_method")

def fetch_scheduled_data() -> pd.DataFrame:
    """
    Connects to a PostgreSQL database and fetches scheduled data.
    Update DB credentials and query accordingly.
    """
    try:
        conn = psycopg2.connect(
            host="localhost",           # Change to your DB host
            port="5432",                # Default PostgreSQL port
            database="your_database",   # Your DB name
            user="your_username",       # Your DB user
            password="your_password"    # Your DB password
        )

        query = "SELECT * FROM your_table_name;"  # Customize this SQL

        logger.info("Executing scheduled PostgreSQL data fetch...")
        df = pd.read_sql_query(query, conn)

        conn.close()
        logger.info("Data fetch successful.")
        return df

    except Exception as e:
        logger.error(f"Error fetching scheduled data: {e}", exc_info=True)
        raise
