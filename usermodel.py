from mongoengine import Document, StringField

class User(Document):
    name = StringField(required=True, max_length=50)
    email = StringField(required=True, max_length=50)
    phone = StringField(required=True, max_length=50)
    countryCode = StringField(required=True, max_length=50)
    password = StringField(required=True, max_length=100)