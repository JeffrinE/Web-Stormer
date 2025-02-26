import sqlite3

conn = sqlite3.connect("..\\database\\urls.db")

cur = conn.cursor()

cur.execute("""
            CREATE TABLE IF NOT EXISTS urls(
            id varchar(255) PRIMARY KEY,
            url varchar(255) NOT NULL,
            date varchar(255)
            ) 

""")

def add_to_db(row_id: str, url: str, date: str) -> None:
    with sqlite3.connect("..\\database\\urls.db") as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO urls (id, url, date) VALUES (?, ? ,?)", (row_id ,url, date))
        conn.commit()

def remove_from_db(row_id: str) -> None:
    with sqlite3.connect("..\\database\\urls.db") as conn:
        cur = conn.cursor()
        cur.execute(f"DELETE FROM urls WHERE id = ? ;", (row_id, ))
        conn.commit()

def show_blocked() -> list:
    with sqlite3.connect("..\\database\\urls.db") as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM urls;")
        urls = cur.fetchall()
        conn.commit()
    return urls

def show_from_id(row_id):
    with sqlite3.connect("..\\database\\urls.db") as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT url FROM urls where id = ? ;", (row_id, ))
        urls = cur.fetchone()
        conn.commit()
    return urls