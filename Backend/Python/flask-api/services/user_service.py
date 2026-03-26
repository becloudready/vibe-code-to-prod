def authenticate_user(username, password):
    return user_repo.get_user_by_credentials(username, password)
# User service layer
import repos.user_repo as user_repo

def create_user(data):
    return user_repo.add_user(data)

def get_users():
    return user_repo.get_all_users()

def get_user(user_id):
    return user_repo.get_user_by_id(user_id)

def update_user(user_id, data):
    return user_repo.update_user(user_id, data)

def delete_user(user_id):
    return user_repo.delete_user(user_id)
