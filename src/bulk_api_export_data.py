import csv
import os
import datetime
from rich import print
from rich.console import Console
from rich.table import Table

from dotenv import load_dotenv
from utils.salesforce_connection import SalesforceConnection
from simple_salesforce import format_soql

load_dotenv()

def init_file(path, column_list):
    directory, filename = os.path.split(path)

    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")

    # Open the file in write mode
    with open(path, mode='w', newline='') as file:
        writer = csv.writer(file, quotechar='"', quoting=csv.QUOTE_ALL)
        
        # Write the header row
        writer.writerow(column_list)

def append_file_with_list(filename, item_list):
    # Open the file in append mode
    with open(filename, mode='a', newline='') as csvfile:
        writer = csv.writer(csvfile, quotechar='"', quoting=csv.QUOTE_ALL)
        
        # Write each item to the file from dict
        for item in item_list:
            csv_items = []
            for item_key, sub_item in item.items():
                csv_items.append(sub_item)
            writer.writerow(csv_items)

def main():
    table = Table(title="Export summary")
    table.add_column("Table", style="green", no_wrap=True)
    table.add_column("CSV file", style="green")
    table.add_column("Record count", justify="right", style="green")

    object_name = 'Account'
    column_list = ['Id','Name','CreatedDate','CreatedBy.Name','LastModifiedDate','LastModifiedBy.Name']
    soql_limit = 10000000

    now = datetime.datetime.now()
    date_string = now.strftime('%Y-%m-%d')

    filename = f"export/{date_string}/{object_name.lower()}.csv"
    sf_connection = SalesforceConnection()

    print('Preparing CSV file with header row:', filename)
    init_file(filename,column_list)

    try:
        sf = sf_connection.get_conn()

        column_str = ','.join(column_list)

        query = f"SELECT {column_str} FROM {object_name} ORDER BY CreatedDate LIMIT {soql_limit}"
        print('Calling BULK API with SOQL:', query)
        # generator on the results page
        fetch_results = sf.bulk.Account.query(query, lazy_operation=True)

        iteration = 0
        total_line_count = 0
        for list_results in fetch_results:
            csv_item_list = []
            for list_item in list_results:
                csv_item = {}
                for item_key, item in list_item.items():
                    if item_key in column_list:
                        if "Date" in item_key and isinstance(item, int):
                            # Convert milliseconds since January 1st 1970 to a UTC datetime
                            seconds = item / 1000
                            dt_object = datetime.datetime.utcfromtimestamp(seconds).replace(tzinfo=datetime.timezone.utc)
                            iso_date_string = dt_object.astimezone(datetime.timezone.utc).isoformat()
                            csv_item[item_key] = iso_date_string
                        else:
                            csv_item[item_key] = item
                    elif item.get('attributes') != None:
                        # Loop through related record attributes to see which ones were needed in column_list
                        for subitem_key, sub_item in item.items():
                            combo_key = f"{item_key}.{subitem_key}"
                            if combo_key in column_list:   
                                csv_item[combo_key] = sub_item     
                csv_item_list.append(csv_item)
            append_file_with_list(filename, csv_item_list)
            iteration += 1
            total_line_count += len(csv_item_list)
            print(f"Processed iteration {iteration}, appended {len(csv_item_list)} rows")
        print(f"Exported total of {total_line_count} rows into {filename}")
        table.add_row(object_name, filename, str(total_line_count))

    except Exception as err:
        print('Failed to fetch data')
        print('Exception type: ', type(err))
        print('Exception args: ', err.args)

    console = Console()
    console.print(table)
    
if __name__ == '__main__':
    main()