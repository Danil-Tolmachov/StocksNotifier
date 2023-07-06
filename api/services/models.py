from pymodm import MongoModel, fields


class User(MongoModel):
    id = fields.IntegerField(primary_key=True)

    email = fields.EmailField()
    phone = fields.CharField()

    consumer_id = fields.IntegerField() # Id of company/delevoper related to user
    external_id = fields.IntegerField() # User id that consumer uses in their own DBs


class Consumer():
    id = fields.IntegerField(primary_key=True)

    username = fields.CharField()
    password = fields.CharField()

    users = fields.ListField()
    access_level = fields.IntegerField()
    template = fields.FileField()

