import sqlite3
import os
import subprocess

def main():
    database_folder = 'db'

    if not os.path.exists(database_folder):
        os.makedirs(database_folder)
        print(f"Created directory: {database_folder}")

    database_path = f"{database_folder}/default.db"
    csv_path = "export/2023-03-30/account.csv"
    table_name = 'account'
    table_create = f'''
    CREATE TABLE {table_name} (
        "Id"  VARCHAR(18) PRIMARY KEY,
        "CreatedDate" TEXT,
        "CreatedByName" TEXT,
        "LastModifiedDate" TEXT,
        "LastModifiedByName" TEXT
    )
    '''

    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        print(f'Dropping table {table_name}')
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        cursor.execute(table_create)

        # Use sqlite .import feature inside subprocess
        print(f'Importing rows from {csv_path} into table {table_name}')
        result = subprocess.run(['sqlite3', database_path, '.mode csv', f'.import --skip 1 {csv_path} {table_name}'], capture_output=True, text=True)
        print(result.stdout)

        cursor.execute(f"CREATE INDEX idx_createdbyname ON {table_name}(CreatedByName)")

        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count_resp = cursor.fetchone()

        print(f'Table created and populated successfully with {count_resp[0]} rows')
        #print(f'sqlite3 {database_path} ".schema {table_name}"')

        conn.commit()

        # Close the cursor and connection
        cursor.close()
        conn.close() 
    except Exception as err:
        print('Failed to import data')
        print('Exception type: ', type(err))
        print('Exception args: ', err.args)
    
if __name__ == '__main__':
    main()