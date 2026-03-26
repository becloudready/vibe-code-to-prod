def get_user_by_credentials(username, password):
    for user in _users:
        if user['username'] == username and user['password'] == password:
            return user
    return None
# User repository layer (in-memory)


# 3 dummy users and 1 admin user
_users = [
    {'id': 1, 'name': 'John Doe', 'age': 22, 'username': 'john', 'password': 'john123'},
    {'id': 2, 'name': 'Jane Smith', 'age': 27, 'username': 'jane', 'password': 'jane123'},
    {'id': 3, 'name': 'Sam Wilson', 'age': 31, 'username': 'sam', 'password': 'sam123'},
    {'id': 4, 'name': 'Admin User', 'age': 35, 'username': 'admin', 'password': 'adminpass', 'role': 'admin'}
]
_next_id = 5

def add_user(user_data):
    global _next_id
    user = {
        'id': _next_id,
        'name': user_data['name'],
        'age': user_data['age'],
        'username': user_data['username'],
        'password': user_data['password']
    }
    _users.append(user)
    _next_id += 1
    return user

def get_all_users():
    return [
        {'id': u['id'], 'name': u['name'], 'age': u['age'], 'username': u['username']} for u in _users
    ]

def get_user_by_id(user_id):
    return next((u for u in _users if u['id'] == user_id), None)

def update_user(user_id, user_data):
    user = get_user_by_id(user_id)
    if not user:
        return None
    user['name'] = user_data.get('name', user['name'])
    user['age'] = user_data.get('age', user['age'])
    user['username'] = user_data.get('username', user['username'])
    user['password'] = user_data.get('password', user['password'])
    return user

def delete_user(user_id):
    global _users
    user = get_user_by_id(user_id)
    if not user:
        return False
    _users = [u for u in _users if u['id'] != user_id]
    return True
