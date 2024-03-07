from peewee import *
from models import *

db = SqliteDatabase("database.db")

def populate_test_database():
    db.connect()
        # Create example users
    address1 = Address.create(Street='Abc', HouseNumber=1, City='Rotterdam', Country = 'Netherlands')
    address2 = Address.create(Street='Xyz', HouseNumber=2, City='Rotterdam', Country = 'Netherlands')

    billInfo1 = BillInfo.create(Currency = 'euro',Street='Abc', HouseNumber=1, City='Rotterdam', Country = 'Netherlands')
    billInfo2 = BillInfo.create(Currency = 'euro',Street='Xyz', HouseNumber=2, City='Rotterdam', Country = 'Netherlands')

    user1 = User.create(name='John Doe', address_key =address1.address_id, bill_info_key = billInfo1.billInfo_id)
    user2 = User.create(name='Jane Clue', address_key =address2.address_id, bill_info_key = billInfo2.billInfo_id)

    # Create example products
    tag1 = Tag.create(Name='Veg')
    tag2 = Tag.create(Name='Meat')
    tag3 = Tag.create(tag_id = 100, Name='Default')

    product1 = Product.create(Name='Potato', Description = 'Fried', Price = 12.99, Quantity = 5, Tag_key = tag1.tag_id)
    product2 = Product.create(Name='Spinach', Description = 'Boiled', Price = 16.99, Quantity = 5, Tag_key = tag1.tag_id)
    product3 = Product.create(Name='Chicken', Description = 'Chinese', Price = 19.99, Quantity = 5, Tag_key = tag2.tag_id)

    # Associate products with users

    user1.products.add([product1, product2])
    user2.products.add([product2, product3])
    
    print("Test database populated successfully.")
    db.close()

if __name__ == "__main__":
    populate_test_database()