import sqlite3

class URLDatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect("database.db")
        self.c = self.conn.cursor()
        self.c.execute("""CREATE TABLE IF NOT EXISTS urls (
                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                              url_name TEXT,
                              long_url TEXT
                          )""")
        
    def findone(self, url_name):
        self.c.execute("SELECT * FROM urls WHERE url_name = ?", (url_name,))
        return self.c.fetchone()
        
    def insertone(self, url_name, long_url):
        self.c.execute("""INSERT INTO urls (url_name, long_url)
                          VALUES (?,?)""", (url_name, long_url))
        self.conn.commit()
        
    def close(self):
        self.conn.close()