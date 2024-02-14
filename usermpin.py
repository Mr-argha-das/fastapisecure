from mongoengine import Document, StringField, DateTimeField
class UserMPIN(Document):
    userid = StringField(required=True, max_lenght=50)
    mpin = StringField(required=True, max_length=50)