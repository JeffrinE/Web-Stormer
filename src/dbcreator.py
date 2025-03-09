import sqlite3
import toml
import platform
import os

with open('pyproject.toml', 'r') as cfg:
    config = toml.load(cfg)
if platform.system() == 'Windows':
    log_path = config['path']['URL_DATABASE_WINDOWS']
elif platform.system() == 'Linux':
    log_path = config['path']['URL_DATABASE_LINUX']

if os.path.exists(log_path):
    conn = sqlite3.connect(log_path)
else:
    conn = sqlite3.connect(log_path)

cur = conn.cursor()


cur.execute("""
            CREATE TABLE IF NOT EXISTS urls(
            id varchar(255) PRIMARY KEY,
            url varchar(255) NOT NULL,
            date varchar(255)
            ) 

""")

def add_to_db(row_id: str, url: str, date: str) -> None:
    with sqlite3.connect(log_path) as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO urls (id, url, date) VALUES (?, ? ,?)", (row_id ,url, date))
        conn.commit()

def remove_from_db(row_id: str) -> None:
    with sqlite3.connect(log_path) as conn:
        cur = conn.cursor()
        cur.execute(f"DELETE FROM urls WHERE id = ? ;", (row_id, ))
        conn.commit()

def show_blocked() -> list:
    with sqlite3.connect(log_path) as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM urls;")
        urls = cur.fetchall()
        conn.commit()
    return urls

def show_from_id(row_id):
    with sqlite3.connect(log_path) as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT url FROM urls where id = ? ;", (row_id, ))
        urls = cur.fetchone()
        conn.commit()
    return urls

def get_uuids():
    with sqlite3.connect(log_path) as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT id FROM urls;")
        urls = cur.fetchall()
        conn.commit()
        append_list = [x[0] for x in urls]
    return append_list