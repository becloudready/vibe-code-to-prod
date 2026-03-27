# User repository layer using MongoDB Atlas
import pymongo
from bson.objectid import ObjectId
from config import MONGODB_URI, DB_NAME

client = pymongo.MongoClient(MONGODB_URI)
db = client[DB_NAME]
users_col = db['users']

def add_user(user_data):
    # user_data should contain: name, age, username, password
    user = {
        'name': user_data['name'],
        'age': user_data['age'],
        'username': user_data['username'],
        'password': user_data['password'],
        'role': user_data.get('role', 'user')
    }
    result = users_col.insert_one(user)
    user['id'] = str(result.inserted_id)
    user.pop('password', None)  # Don't return password
    return user

def get_all_users():
    users = list(users_col.find())
    for user in users:
        user['id'] = str(user['_id'])
        user.pop('_id', None)
        user.pop('password', None)  # Don't expose passwords
    return users

def get_user_by_id(user_id):
    user = users_col.find_one({'_id': ObjectId(user_id)})
    if user:
        user['id'] = str(user['_id'])
        user.pop('_id', None)
        user.pop('password', None)
        return user
    return None

def update_user(user_id, user_data):
    update_fields = {k: v for k, v in user_data.items() if k in ['name', 'age', 'username', 'password', 'role']}
    result = users_col.update_one({'_id': ObjectId(user_id)}, {'$set': update_fields})
    if result.matched_count:
        return get_user_by_id(user_id)
    return None

def delete_user(user_id):
    result = users_col.delete_one({'_id': ObjectId(user_id)})
    return result.deleted_count > 0

def get_user_by_credentials(username, password):
    user = users_col.find_one({'username': username, 'password': password})
    if user:
        user['id'] = str(user['_id'])
        user.pop('_id', None)
        user.pop('password', None)
        return user
    return None
