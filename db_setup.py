import sqlite3
import os

class DataBaseWork:
    def __init__(self):
        ld = os.listdir(os.getcwd())
        self.path_to_database = 'moneys.db'
        if 'moneys.db' not in ld:
            self.setup_db()

    def setup_db(self):
        conn = sqlite3.connect(self.path_to_database)
        conn.cursor().execute("""CREATE TABLE moneys(
                                                    user_id TEXT UNIQUE,
                                                    current_balance FLOAT
                                                        )""")
        conn.close()

    def add_or_spend_money(self, user_id, money, money_state):
        conn = sqlite3.connect(self.path_to_database)
        if conn.cursor().execute("""SELECT * FROM moneys WHERE user_id = ?""", (user_id,)).fetchall():
            if money_state:
                conn.cursor().execute("""UPDATE moneys SET current_balance = current_balance + ? WHERE user_id = ?
                                                    """, (money, user_id))
            else:
                conn.cursor().execute("""UPDATE moneys SET current_balance = current_balance - ? WHERE user_id = ?
                                                                    """, (money, user_id))
        else:
            if money_state:
                conn.cursor().execute("""INSERT INTO moneys VALUES(?, ?)""", (user_id, money))
            else:
                conn.cursor().execute("""INSERT INTO moneys VALUES(?, ?)""", (user_id, -money))
        conn.commit()
        conn.close()

    def get_balance(self, user_id):
        conn = sqlite3.connect(self.path_to_database)
        balance = conn.cursor().execute("""SELECT current_balance FROM moneys WHERE user_id = ?
                              """, (user_id,)).fetchall()
        conn.close()
        return balance

