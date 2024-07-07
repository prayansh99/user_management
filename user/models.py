from .mongo_connection import db
from bson.objectid import ObjectId

# client = MongoClient(settings.MONGODB_URI)
# db = client.get_database(settings.MONGO_DB_NAME)
# users_collection = db['mydatabase']
# users_collection = db['Users']


class CustomModelException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class User:
    # collection = db.users
    collection = db['Users']
    @staticmethod
    def create_user(data):
        return User.collection.insert_one(data)

    @staticmethod
    def find_by_email(email):
        return User.collection.find_one({"email": email})

    @staticmethod
    def find_by_username(username):
        return User.collection.find_one({"username": username})

    @staticmethod
    def find_by_id(user_id):
        try:
            return User.collection.find_one({"_id": ObjectId(user_id)})
        except Exception as e:
            raise CustomModelException("User_id invalid.")

