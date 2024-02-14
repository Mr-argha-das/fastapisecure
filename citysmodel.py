from mongoengine import Document, StringField

class CityModel(Document):
    cityname = StringField(required=True, max_length=200)
    