# Imports
import argparse
import csv
import datetime
import os
from datetime import datetime, timedelta
from decimal import Decimal
from itertools import groupby
from item import Item
from reportGen import ReportGen

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"

def buy_product(product_name, price, expiration_date, date):
    # Add your logic for buying the product here
    succeed = False
    if os.path.exists("bought.csv"):
    # Append data to the existing CSV file
        id = 0
        with open('bought.csv', 'r') as file:
            lines = file.readlines()
            if lines:
                last_line = lines[-1].strip()
                id = int(last_line.split()[4])
        with open('bought.csv', mode='a', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
            id = id+ 1
            spamwriter.writerow([product_name, price, expiration_date, date, id])
            succeed = True
    else:
    # Create a new CSV file and write data
        with open('bought.csv', mode='w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=' ',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow([product_name, 1, price, expiration_date, date])
            succeed = True
    if succeed:
        print("Successfully bought the product!")
        
def sell_product(product_name, price, date):
    obj = CanSell(product_name)
    succeed = False
    if obj is None:
        print("SORRY: Product not in stock. ")
    else:
        if os.path.exists("sold.csv"):
            with open('sold.csv', mode='a', newline='') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=' ',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerow([product_name, obj.price, price, date, obj.id])
                succeed = True
        else:
        # Create a new CSV file and write data
            with open('sold.csv', mode='w', newline='') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=' ',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerow([product_name, price, date])
                succeed = True
    if succeed:
        print("Successfully sold the product!")
def advance_time(days):
    try:
        # Read current time from the file or set a default time
        with open("current_time.txt", "r") as file:
            current_time_str = file.read()
            current_time = datetime.strptime(current_time_str, "%Y-%m-%d")
    except FileNotFoundError:
        current_time = datetime.now()

    # Advance time by the specified number of days
    new_time = current_time + timedelta(days=days)

    # Save the new time to the file
    with open("current_time.txt", "w") as file:
        file.write(new_time.strftime("%Y-%m-%d"))

    print(f"Time advanced by {days} days. New time: {new_time}")
    return new_time.strftime("%Y-%m-%d")

def now_Or_Yesterday(now=False, yesterday=False):
    try:
        # Read current time from the file or set a default time
            with open("current_time.txt", "r") as file:
                current_time_str = file.read()
                current_time = datetime.strptime(current_time_str, "%Y-%m-%d")
    except FileNotFoundError:
        current_time = datetime.now()

    if now:
        current_time = datetime.now()
    elif yesterday:
        current_time = current_time - timedelta(days=1)
    
    with open("current_time.txt", "w") as file:
        file.write(current_time.strftime("%Y-%m-%d"))

    return current_time.strftime("%Y-%m-%d")

def read_items_from_file(product, file_name, bought=False, sold=False):
        items = []
        try:
            with open(file_name, 'r') as file:
                for line in file:
                    split_result = line.split()
                    if split_result[0] == product:
                        if bought:
                            items.append(Item(split_result[0], split_result[1], split_result[3], None, split_result[4]))
                        elif sold:
                            items.append(Item(split_result[0], split_result[1], None, split_result[2], split_result[4]))
        except FileNotFoundError:
            print(f"File not found: {file_name}")
        except Exception as e:
            print(f"An error occurred: {e}")
        return items

def CanSell(product):
    bought = read_items_from_file(product, "bought.csv", bought=True)
    sold = read_items_from_file(product, "sold.csv", sold=True)

    new_bought = [b for b in bought if not any(b.id == s.id for s in sold)]   
    if new_bought:
        sorted_items = sorted(new_bought, key=lambda x: x.price)
        return sorted_items[0]
    else:
       return None
def main():
    # Create ArgumentParser object
    parser = argparse.ArgumentParser(description="Super script for buying or selling products")

    # Add arguments
    parser.add_argument("action", nargs='?', choices=["buy", "sell", "report"], help="Action to perform")

    parser.add_argument("--product-name", nargs='?', required=False, help="Name of the product")
    parser.add_argument("--price", nargs='?', type=float, required=False, help="Price of the product")

    # Expiration date is required only for the "buy" action
    parser.add_argument("--expiration-date", required=False, help="Expiration date of the product")
    parser.add_argument("--advance-time", required=False, type=int, help="Number of days to advance time")
    parser.add_argument("--now", required=False, action="store_true", help="Report inventory as of the current time")
    parser.add_argument("--yesterday", required=False, action="store_true", help="Report inventory as of the yesterday time")
    parser.add_argument('report_type',nargs='?', choices=['inventory','revenue', 'profit', 'chart'], help='The type of report to generate')

    # Parse the command line arguments
    args = parser.parse_args()
    if args.yesterday:
        _current = now_Or_Yesterday(now=False, yesterday=True)
    elif args.advance_time is not None:
        _current = advance_time(args.advance_time)
    elif args.now:
         _current = now_Or_Yesterday(now=True)
    else:
         _current = now_Or_Yesterday()
    # Perform actions based on the provided arguments
    reportGen_instance = ReportGen(_current)
    if args.action == "buy":
        if not args.expiration_date:
            parser.error("Expiration date is required for the 'buy' action.")
        buy_product(args.product_name, args.price, args.expiration_date, _current)
    elif args.action == "sell":
        sell_product(args.product_name, args.price, _current)
    elif args.action ==  "report" and args.report_type == "inventory":
        reportGen_instance.show_Inventory()
    elif args.action ==  "report" and args.report_type == "revenue":
        reportGen_instance.getRevenue()
    elif args.action ==  "report" and args.report_type == "profit":
        reportGen_instance.getProfit()
    elif args.action ==  "report" and args.report_type == "chart":
        reportGen_instance.show_Inventory_InChart()
if __name__ == "__main__":
    main()
