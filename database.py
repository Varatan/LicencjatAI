import dbOps

conn = dbOps.get_db_connection()
print("Connected to database successfully")
conn.execute('''CREATE TABLE IF NOT EXISTS requests (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        race TEXT,
                        gender TEXT,
                        alignment TEXT,
                        profession TEXT,
                        tone TEXT,
                        culture TEXT,
                        last name TEXT,
                        nickname TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )''')
print("Created table 1 successfully!")

conn.execute('''CREATE TABLE IF NOT EXISTS responses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        requestID INTEGER,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY(requestID) REFERENCES requests(id)
                    )''')
print("Created table 2 successfully!")

conn.close()