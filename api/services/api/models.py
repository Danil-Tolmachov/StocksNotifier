from pymodm import MongoModel, fields
from pymodm.manager import Manager
from pymongo.write_concern import WriteConcern
from pymodm.connection import connect

from services.api.utils import hash_password


connect("mongodb://root:test@localhost/checkers_db?authSource=admin", alias='my-app')


class CustomManager(Manager):
    def create(cls, **kwargs):
        username = kwargs.get('username')

        # Username unique check
        if username is not None:
            try:
                if isinstance(cls.get({'username': username}), MongoModel):
                    raise ValueError('Username field is not unique')
            except:
                pass

        obj = super().create(**kwargs)

        # Hashing password
        if obj.password is not None:
            password = obj.password
            obj.password = hash_password(password)

        obj.save()


class User(MongoModel):
    id = fields.IntegerField(primary_key=True)

    username = fields.CharField()
    password = fields.CharField()

    email = fields.EmailField()
    phone = fields.CharField()

    consumer_id = fields.IntegerField() # Relation user to developer
    external_id = fields.IntegerField() # User id that consumer uses in their own DBs   

    objects = CustomManager()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'my-app'
        
    @classmethod
    def get_next_id(cls):
        # Get the highest existing ID
        max_id = cls.objects.aggregate({"$group": {"_id": None, "max_id": {"$max": "$_id"}}})
        if max_id.alive:
            return max_id.next()["max_id"] + 1
        else:
            return 1

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.get_next_id()
        return super(User, self).save(*args, **kwargs)

class Developer(MongoModel):
    id = fields.IntegerField(primary_key=True)

    username = fields.CharField()
    password = fields.CharField()

    users = fields.ListField()
    access_level = fields.IntegerField()
    html_template = fields.FileField()

    objects = CustomManager()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'my-app'

    @classmethod
    def get_next_id(cls):
        # Get the highest existing ID
        max_id = cls.objects.aggregate({"$group": {"_id": None, "max_id": {"$max": "$_id"}}})
        if max_id.alive:
            return max_id.next()["max_id"] + 1
        else:
            return 1

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.get_next_id()
        return super(Developer, self).save(*args, **kwargs)
