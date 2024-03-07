from peewee import *
from models import *
from datetime import datetime

# Do not modify these lines
__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

# Add your code after this line
db = SqliteDatabase("database.db")

def search(term):
    db.connect()
    matching_products = Product.select().where(fn.lower(Product.Name).contains(term.lower()))
    for product in matching_products:
        print(product.Name)
    db.close()
def list_user_products(user_id):
    db.connect()
    user = User.get(User.user_id == user_id)
    user_products = user.products
    for product in user_products:
        print(product.Name)
    db.close()
def list_products_per_tag(tag_id):
    db.connect()
    products = Product.select().where(Product.Tag_key == tag_id)

    for product in products:
        print(product.Name)

    db.close()
def add_catalog(name):
    db.connect()
    try:
        tag = Tag.create(Name=name)
        print(f"Tag '{name} tag.tag_id' added.")
    except Tag.DoesNotExist:
        print("Tag not found.")
    db.close()

def add_product_to_catalog(product, desc, price, tag, quantity):
    db.connect()
    try:
        tag = Tag.get_by_id(tag)
        product1 = Product.create(Name=product, Description = desc, Price = price, Quantity = quantity, Tag_key = tag.tag_id)
        print(f"Product '{product1.Name}' added to the catalog.")
    except Tag.DoesNotExist:
        print("Tag not found.")
    db.close()

def add_product_to_user(user_id, product):
    db.connect()
    try:
        user = User.get_by_id(user_id)
        product = Product.get(Name=product)
        user.products.add(product)
        print(f"Product '{product.Name}' added to the user.")
    except User.DoesNotExist:
        print("User not found.")
    except Product.DoesNotExist:
        print("User not found.")
    db.close()

def update_stock(product_id, new_quantity):
    db.connect()
    try:
        product = Product.get_by_id(product_id)
        product.Quantity = new_quantity
        product.save()
        print(f"Product '{product}' quantity updated.")
    except Product.DoesNotExist:
        print("Product not found.")
    db.close()


def purchase_product(product_id, buyer_id, quantity):
    db.connect()
    try:
        product = Product.get_by_id(product_id)
        buyer = User.get_by_id(buyer_id)
        Transaction.create(Date=datetime.now(),user_key = buyer_id, product_key=product_id, quantity = quantity)
        print(f"Transaction created.")
    except Product.DoesNotExist:
        print("Product not found.")
    except User.DoesNotExist:
        print("Buyer not found.")
    db.close()


def remove_product(product_id):
    db.connect()
    try:
        Product.delete_by_id(product_id)
        print(f"Product deleted.")
    except Product.DoesNotExist:
        print("Product not found.")
    db.close()
