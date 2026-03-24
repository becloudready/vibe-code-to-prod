# User repository layer (in-memory)

_users = [
    {'id': 1, 'name': 'Alice', 'age': 30, 'username': 'alice', 'password': 'alicepass'},
    {'id': 2, 'name': 'Bob', 'age': 25, 'username': 'bob', 'password': 'bobpass'},
    {'id': 3, 'name': 'Charlie', 'age': 28, 'username': 'charlie', 'password': 'charliepass'}
]
_next_id = 4

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
