from pymodm import MongoModel, fields


class User(MongoModel):
    id = fields.IntegerField(primary_key=True)

    email = fields.EmailField()
    phone = fields.EmailField()

    consumer_id = fields.IntegerField() # Id of company/delevoper related to user
    external_id = fields.IntegerField() # User id that consumer uses in their own DBs

