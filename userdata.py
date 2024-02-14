from mongoengine import Document, StringField, DateTimeField
from datetime import datetime
class UserContacts(Document):
    userid = StringField(required=True, max_length=50)
    userData = StringField(required=True, max_length=100)
    date = DateTimeField(default=datetime.today())