import sqlite3

import src.api.Utils as Utils
from src.api.Config import Config
from src.api.Entry import Entry


class Database:
    def __init__(self, config: Config):
        self.file = Utils.get_dir() + config.get('db.file')
        self.db = sqlite3.connect(self.file)
        self.cur = self.db.cursor()

        self.init_db()

    def init_db(self):
        self.cur.execute('CREATE TABLE IF NOT EXISTS users (uid text, username text, hash text)')
        self.db.commit()

    def add_user(self, uid: str, username: str, hashed: str):
        self.cur.execute(f'''CREATE TABLE {"user_" + uid} 
            (uid text, name text, description text, username text, password text, nonce text, tag text)''')
        self.cur.execute('INSERT INTO users VALUES (?, ?, ?)', (uid, username, hashed))
        self.db.commit()

    def delete_user(self, uid: str):
        self.cur.execute(f'DROP TABLE {"user_" + uid}')
        self.cur.execute(f'DELETE FROM users WHERE uid = ?', (uid,))
        self.db.commit()

    # def get_user_by_uid(self, uid: str):
    #     return self.cur.execute('SELECT * FROM users WHERE uid = ?', (uid,)).fetchone()

    def get_user_by_username(self, username: str):
        return self.cur.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

    def update_hash(self, uid: str, hashed: str):
        self.cur.execute(f'UPDATE users SET hash = ? WHERE uid = ?', (hashed, uid))
        self.db.commit()

    def add_account(self, uid: str, entry: Entry):
        data = (entry.uid, entry.name, entry.description, entry.username, entry.password, entry.nonce, entry.tag)
        self.cur.execute(f'INSERT INTO {"user_" + uid} VALUES (?, ?, ?, ?, ?, ?, ?)', data)
        self.db.commit()

    def delete_account(self, uid: str, account_id: str):
        self.cur.execute(f'DELETE FROM {"user_" + uid} WHERE uid = ?', (account_id,))
        self.db.commit()

    def get_accounts(self, uid: str, query: str):
        return self.cur.execute(
            f'''
                SELECT uid, name, description FROM {"user_" + uid} WHERE name LIKE :query
                OR description LIKE :query OR username LIKE :query
            ''',
            {'query': f'%{query}%'}
        ).fetchall()

    def get_account_by_uid(self, uid: str, account_id: str):
        return self.cur.execute(f'SELECT * FROM {"user_" + uid} WHERE uid = ?', (account_id,)).fetchone()
