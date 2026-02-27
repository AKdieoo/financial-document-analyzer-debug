import sqlite3

DB_NAME = "analysis.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            query TEXT,
            result TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_analysis(filename, query, result):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO analyses (filename, query, result) VALUES (?, ?, ?)",
        (filename, query, str(result))
    )

    conn.commit()
    conn.close()