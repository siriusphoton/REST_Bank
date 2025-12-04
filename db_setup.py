import sqlite3

def init_db():
    conn = sqlite3.connect('bank_app.db')
    cursor = conn.cursor()
    cursor.execute(''' DROP TABLE IF EXISTS accounts''')
    cursor.execute('''
                   CREATE TABLE accounts(
                        id INTEGER PRIMARY KEY,
                        username TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL,
                        balance REAL DEFAULT 0.0
                   );
                ''')
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS nominees(
                        id INTEGER PRIMARY KEY,
                        account_id INTEGER NOT NULL,
                        full_name TEXT NOT NULL,
                        relation TEXT NOT NULL,
                        FOREIGN KEY (account_id) REFERENCES accounts(id)
                   );
                ''')
    conn.commit()
    conn.close()
if __name__ == '__main__':
    init_db()
    print("Database is setup good to go.")