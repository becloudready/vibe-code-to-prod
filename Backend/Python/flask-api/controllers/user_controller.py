
# User controller layer
from flask import Blueprint, request, jsonify
import services.user_service as user_service

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = user_service.authenticate_user(username, password)
    if user:
        return jsonify({'success': True, 'user': {'id': user['id'], 'username': user['username'], 'role': user.get('role', 'user')}})
    else:
        return jsonify({'success': False, 'message': 'Invalid username or password'}), 401

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = user_service.create_user(data)
    return jsonify({'id': user['id']}), 201

@user_bp.route('/users', methods=['GET'])
def get_users():
    users = user_service.get_users()
    return jsonify(users)

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = user_service.get_user(user_id)
    # ...existing code...

# Endpoint to match frontend call for getAllUsers
@user_bp.route('/getAllUsers', methods=['GET'])
def get_all_users():
    users = user_service.get_users()
    return jsonify(users)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'id': user['id'], 'name': user['name'], 'age': user['age'], 'username': user['username']})

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = user_service.update_user(user_id, data)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'message': 'User updated'})

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    success = user_service.delete_user(user_id)
    if not success:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'message': 'User deleted'})
