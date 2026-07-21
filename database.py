import sqlite3

conn = sqlite3.connect("videos.db", check_same_thread=False)
db = conn.cursor()

db.execute("""
CREATE TABLE IF NOT EXISTS videos (
    code TEXT PRIMARY KEY,
    file_id TEXT NOT NULL
)
""")

conn.commit()


def save_video(code, file_id):
    db.execute(
        "INSERT OR REPLACE INTO videos (code, file_id) VALUES (?, ?)",
        (code, file_id)
    )
    conn.commit()


def get_video(code):
    db.execute("SELECT file_id FROM videos WHERE code=?", (code,))
    row = db.fetchone()
    return row[0] if row else None
