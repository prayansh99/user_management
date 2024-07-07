import pymongo
from django.conf import settings

client = pymongo.MongoClient(settings.MONGODB_URI)
db = client[settings.MONGO_DB_NAME]