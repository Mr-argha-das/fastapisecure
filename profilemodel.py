from mongoengine import Document, StringField

class UserProfile(Document):
    user_id = StringField(required=True, max_length=50)
    upiId = StringField(required=True, max_length=50)
    profileImage = StringField(required=False, max_length=100)
    gender = StringField(required=True, max_length=50)
    age = StringField(required=True, max_length=50)
    location = StringField(required=True, max_length=50)