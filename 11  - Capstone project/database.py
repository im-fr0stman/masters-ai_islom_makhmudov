import sqlite3
import logging
from config import DATABASE_PATH, LOG_FILE

# ✅ Configure Logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    try:
        conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
        return conn
    except sqlite3.Error as e:
        logging.error(f"Database connection failed: {e}")
        return None

def execute_query(query, params=()):
    """Executes a secure SQL query with parameterized inputs."""
    conn = get_db_connection()
    if not conn:
        return "Database connection error."
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)  # ✅ Prevents SQL Injection
        results = cursor.fetchall()
        conn.commit()
        conn.close()
        return results if results else "No results found."
    except sqlite3.Error as e:
        logging.error(f"SQL execution error: {e}")
        return f"SQL Error: {e}"

# ✅ Example Usage
if __name__ == "__main__":
    sample_query = "SELECT * FROM countries WHERE region = ? LIMIT 5"
    region = ("Europe",)
    print(execute_query(sample_query, region))
