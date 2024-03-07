import argparse
import csv
import datetime
import os
from datetime import datetime, timedelta
from decimal import Decimal
from itertools import groupby
from item import Item
from productChartInfo import ProductChartInfo
from rich.console import Console
from rich.table import Table
import matplotlib.pyplot as plt

class ReportGen:
    def __init__(self, current_time):
        self.current_time = current_time
    
    def getRevenue(self):
        sold = []
        inventory = []
        try:
            with open("sold.csv", 'r') as file:
                for line in file:
                    split_result = line.split()
                    current_object = datetime.strptime(self.current_time, "%Y-%m-%d")
                    date_object = datetime.strptime(split_result[3], "%Y-%m-%d")
                    if date_object <= current_object:
                        sold.append(Item(split_result[0], split_result[1], None, split_result[2], split_result[4]))
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"An error occurred: {e}")

        revenue = 0
        for s in sold:
            revenue = revenue + Decimal(s.price)
    
        print(f"Revenue so far {revenue}")

    def getProfit(self):
        sold = []
        try:
            with open("sold.csv", 'r') as file:
                for line in file:
                    split_result = line.split()
                    current_object = datetime.strptime(self.current_time, "%Y-%m-%d")
                    date_object = datetime.strptime(split_result[3], "%Y-%m-%d")
                    if date_object <= current_object:
                        sold.append(Item(split_result[0], split_result[1], None, split_result[2], split_result[4]))
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"An error occurred: {e}")

        revenue = 0
        salePrice = 0
        for s in sold:
            revenue = revenue + Decimal(s.salePrice)
            salePrice = salePrice + Decimal(s.price)
        print(f"Profit so far {abs(revenue - salePrice)}")
  
    def show_Inventory(self):
        bought = []
        sold = []
        inventory = []
        try:
            with open("bought.csv", 'r') as file:
                for line in file:
                    split_result = line.split()
                    current_object = datetime.strptime(self.current_time, "%Y-%m-%d")
                    bought.append(Item(split_result[0], split_result[1], split_result[3], None, split_result[4]))
            with open("sold.csv", 'r') as file:
                for line in file:
                    split_result = line.split()
                    current_object = datetime.strptime(self.current_time, "%Y-%m-%d")
                    sold.append(Item(split_result[0], split_result[1], None, split_result[2], split_result[4]))
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"An error occurred: {e}")

        console = Console()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Product Name", style="dim", width=12)
        table.add_column("Count")
        table.add_column("Buy Price", justify="right")
        table.add_column("Expiration Date", justify="right")
        for b in bought:
            avail = True
            for s in sold:
                if s.id==b.id:
                    avail = False
            if avail:
                table.add_row(f" {b.name}", "1" , f"{b.price} ",f"{b.expiration_date}")  # .strip() removes any leading or trailing whitespace
        console.print(table)

    def show_Inventory_InChart(self):
        bought = []
        sold = []
        inventory = []
        colors = {}
        try:
            with open("bought.csv", 'r') as file:
                for line in file:
                    split_result = line.split()
                    current_object = datetime.strptime(self.current_time, "%Y-%m-%d")
                    bought.append(Item(split_result[0], split_result[1], split_result[3], None, split_result[4]))
            with open("sold.csv", 'r') as file:
                for line in file:
                    split_result = line.split()
                    current_object = datetime.strptime(self.current_time, "%Y-%m-%d")
                    sold.append(Item(split_result[0], split_result[1], None, split_result[2], split_result[4]))
            with open("products.csv", 'r') as file:
                for line in file:
                    split_result = line.split()
                    name = split_result[0]
                    color = split_result[1]
                    colors[name] = color
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"An error occurred: {e}")

        bought_counts = {}
        sold_counts = {}

        for b in bought:
            if b in bought_counts:
                bought_counts[b] += 1
            else:
                bought_counts[b] = 1
        for s in sold:
            if s in sold_counts:
                sold_counts[s] += 1
            else:
                sold_counts[s] = 1
            for item, count in bought_counts.items():
                if item.id == s.id:
                    bought_counts[item] = bought_counts[item] -1
        products = {}
        for item, count in bought_counts.items():
            if item.name not in products:
                products[item.name] = ProductChartInfo(0,"")
            products[item.name].count = products[item.name].count+ count
            for name, color in colors.items():
                if name == item.name:
                    products[item.name].color= color
                    break

        product_names = []
        product_counts = []
        product_colors = []

        for product_name, product_info in products.items():
            product_names.append(product_name)
            product_counts.append(product_info.count)
            product_colors.append(f"tab:{product_info.color}")
        fig, ax = plt.subplots()

        ax.bar(product_names, product_counts, label=product_names, color=product_colors)

        ax.set_ylabel('fruit supply')
        ax.set_title('Fruit supply by kind and color')
        ax.legend(title='Fruit color')

        plt.show()