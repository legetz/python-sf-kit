import os
import sqlite3

def connect_db(db_path = None):
    database_path = None
    if(db_path != None):
        database_path = db_path
    else:
        database_path = os.environ.get("DB_NAME", 'db/default.db')
    print(f'Connecting to database {database_path}')
    return sqlite3.connect(database_path)
