from mongoengine import Document, StringField, DateTimeField, IntField, BooleanField
from datetime import datetime

class UserWithdrawal(Document):
    userid = StringField(required=True, max_length=50)
    trnx = StringField(required=False, max_length=50)
    amount = StringField(required=True, max_length=200)
    status = BooleanField(required=True)
    creatat = DateTimeField(default=datetime.today())
    updateat = DateTimeField(default=datetime.today())
    