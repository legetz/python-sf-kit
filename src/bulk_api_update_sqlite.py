from dotenv import load_dotenv
from utils.salesforce_connection import SalesforceConnection
from config.database import connect_db

load_dotenv()

def main():
    table_name = 'account'

    try:
        conn = connect_db()
        cursor = conn.cursor()

        sql_query = f"SELECT Id,Name FROM {table_name} LIMIT 10"
        cursor.execute(sql_query)
        results = cursor.fetchall()
        print(f'Found {len(results)} rows for query {sql_query}')
        update_list = []

        for row in results:
            sf_id, sf_name = row
            sf_entry = {
                'Id': sf_id,
                'Name': sf_name
            }
            update_list.append(sf_entry)

        if(len(update_list) == 0):
            cursor.close()
            conn.close() 
            return

        batch_size = 10000
        use_serial = True
        print(f'Updating records using BULK API [batch_size={batch_size},use_serial={use_serial}]')
        sf_connection = SalesforceConnection()
        sf = sf_connection.get_conn()
        bulk_resp = sf.bulk.Account.update(update_list,batch_size=10000,use_serial=True)
        for resp_item in bulk_resp:
            if(resp_item['success'] == True):
                print(f'Updated record {resp_item["id"]}')
                cursor.execute(f'UPDATE account SET UpdateSuccess=1 WHERE Id=\'{resp_item["id"]}\' LIMIT 1')
            else:
                print(f'Failed to update record: {resp_item}')
        
        conn.commit()

        # Close the cursor and connection
        cursor.close()
        conn.close() 
    except Exception as err:
        print('Failed to update data')
        print('Exception type: ', type(err))
        print('Exception args: ', err.args)
    
if __name__ == '__main__':
    main()