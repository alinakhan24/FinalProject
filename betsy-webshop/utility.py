from peewee import *
from models import *

db = SqliteDatabase("database.db")

def create_tables():
    with db:
        db.create_tables([Address, BillInfo, Tag, Product, User, UserProduct, Transaction])


if __name__ == "__main__":
    create_tables()