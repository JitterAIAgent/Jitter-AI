import sqlite3
import os

def setup_database(db_name="agent_memory.db"):
    conn = None # Initialize connection to None

    try:
        db_path = os.path.join(os.path.dirname(__file__), db_name)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        print(f"Successfully connected to database: {db_name}")

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                context_id TEXT NOT NULL,
                message TEXT NULL,
                role TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Commit the changes to the database
        conn.commit()

        print("DB setup complete.")

    except sqlite3.Error as e:
        raise Exception(f"An SQLite error occurred: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    setup_database()
