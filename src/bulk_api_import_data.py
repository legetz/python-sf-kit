from dotenv import load_dotenv
from salesforce_connection import SalesforceConnection
from simple_salesforce import format_soql

load_dotenv()

def main():
    sf_connection = SalesforceConnection()

    try:
        sf = sf_connection.get_conn()

        query = "SELECT Id, CreatedDate FROM Account"
        print('Calling BULK API with SOQL:', query)
        # generator on the results page
        fetch_results = sf.bulk.Account.query(query, lazy_operation=True)

        # the generator provides the list of results for every call to next()
        all_results = []
        iteration = 0
        for list_results in fetch_results:
            for list_item in list_results:
                print(list_item)
            all_results.extend(list_results)
            iteration += 1
            print(f"Processed iteration {iteration}")
    except Exception as err:
        print('Failed to fetch data')
        print('Exception type: ', type(err))
        print('Exception args: ', err.args)
    
if __name__ == '__main__':
    main()