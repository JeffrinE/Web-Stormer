import sqlite3
import toml
import platform
import os
import hashlib

with open('pyproject.toml', 'r') as cfg:
    config = toml.load(cfg)
if platform.system() == 'Windows':
    log_path = config['path']['CRED_DATABASE_WINDOWS']
elif platform.system() == 'Linux':
    log_path = config['path']['CRED_DATABASE_LINUX']

if os.path.exists(log_path):
    conn = sqlite3.connect(log_path)
else:
    conn = sqlite3.connect(log_path)

cur = conn.cursor()

cur.execute("""
            CREATE TABLE IF NOT EXISTS users(
            user varchar(255) PRIMARY KEY,
            passwd varchar(255) NOT NULL
            )
""")


def add_to_db(user: str, passwd: str) -> None:
    with sqlite3.connect(log_path) as conn:
        cur = conn.cursor()
        cur.execute("INSERT OR REPLACE INTO users (user, passwd) VALUES (?, ? );", (user, passwd))
        conn.commit()

def is_user_in_db(user:str, passwd: str) -> bool:
    with sqlite3.connect(log_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT passwd FROM users WHERE user = (?);", (user, ))
        password = cur.fetchone()
        conn.commit()
        if password == None:
            pass
        else:
            auth = passwd.encode()
            auth_hash = hashlib.sha256(auth).hexdigest()
            if password[0] == auth_hash:
                return True
            else:
                return False
        
def change_password(user: str, og_passwd: str, new_passwd: str, confirm_passwd: str):
    with sqlite3.connect(log_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT passwd FROM users WHERE user = (?);", (user, ))
        password = cur.fetchone()
        conn.commit()
        if (og_passwd == password[0]):
            if (new_passwd == confirm_passwd):
                auth = new_passwd.encode()
                auth_hash = hashlib.sha256(auth).hexdigest()
                cur.execute("UPDATE users SET passwd = (?) WHERE user = (?);", (auth_hash, user))
                print(f"New passwd set {new_passwd}")
                return True
        else:
            print("An Error has occured during password change")
            return False


auth = "1234".encode()
auth_hash = hashlib.sha256(auth).hexdigest()
add_to_db("admin", auth_hash)