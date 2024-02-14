from mongoengine import Document, StringField, DateTimeField
from datetime import datetime

class ProjectsModel(Document):
    projectTitle = StringField(required=True, max_length=50)
    url = StringField(required=True, max_length=50)
    location = StringField(required=True, max_length=56)
    date = DateTimeField(default=datetime.today())