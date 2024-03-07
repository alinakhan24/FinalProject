import peewee

db = peewee.SqliteDatabase("database.db")


class Address(peewee.Model):
    address_id = peewee.AutoField(primary_key=True)
    Street = peewee.CharField()
    HouseNumber = peewee.IntegerField()
    City = peewee.CharField()
    Country = peewee.CharField()

    class Meta:
        database = db

class BillInfo(peewee.Model):
    billInfo_id = peewee.AutoField(primary_key=True)
    Currency = peewee.CharField()
    Street = peewee.CharField()
    HouseNumber =peewee.IntegerField()
    City = peewee.CharField()
    Country = peewee.CharField()

    class Meta:
        database = db

class Tag(peewee.Model):
    tag_id = peewee.AutoField(primary_key=True)
    Name = peewee.CharField(unique=True)
    class Meta:
        database = db

class Product(peewee.Model):
    product_id = peewee.AutoField(primary_key=True)
    Name = peewee.CharField()
    Description = peewee.CharField(null=True)
    Price = peewee.DecimalField(default=10.99)
    Quantity = peewee.IntegerField(default=1)
    Tag_key = peewee.ForeignKeyField(Tag)
    class Meta:
        database = db

class User(peewee.Model):
    user_id = peewee.AutoField(primary_key=True)
    name = peewee.CharField()
    address_key = peewee.ForeignKeyField(Address)
    bill_info_key = peewee.ForeignKeyField(BillInfo)
    products = peewee.ManyToManyField(Product)

    class Meta:
        database = db

class Transaction(peewee.Model):
    transaction_id = peewee.AutoField(primary_key=True)
    Date = peewee.DateField()
    user_key = peewee.ForeignKeyField(User)
    product_key = peewee.ForeignKeyField(Product)
    quantity = peewee.IntegerField()
    class Meta:
        database = db

class UserProduct(peewee.Model):
    user = peewee.ForeignKeyField(User)
    product = peewee.ForeignKeyField(Product)

    class Meta:
        database = db

UserProduct = User.products.get_through_model()


