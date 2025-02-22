import sqlite3

conn = sqlite3.connect(r"..\database\urls.db")

cur = conn.cursor()

cur.execute("""
            CREATE TABLE IF NOT EXISTS urls(
            id INTEGER PRIMARY KEY,
            url varchar(255) NOT NULL,
            date text
            ) 

""")
# cur.execute("INSERT INTO urls (url, date) VALues (?, ?)", ("www.example.com", "1234.32.32"))

def add_to_db(url: str, date: str) -> None:
    with sqlite3.connect(r"..\database\urls.db") as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO urls (url, date) VALUES ( ? , ?)", (url, date))
        conn.commit()

def remove_from_db(url: str) -> None:
    with sqlite3.connect(r"..\database\urls.db") as conn:
        cur = conn.cursor()
        cur.execute(f"DELETE FROM urls WHERE url = ? ;", (url, ))
        conn.commit()

def show_blocked() -> list:
    with sqlite3.connect(r"..\database\urls.db") as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM urls;")
        conn.commit()
        urls = cur.fetchall()
    return urls