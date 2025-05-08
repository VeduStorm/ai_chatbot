import os
import json
import hashlib
import sys
from easygui import passwordbox, enterbox

CHAT_HISTORY_DIR = 'chat_histories'
AUTH_FILE = 'auth.json'

def initialize_auth_system():
    """Initialize the authentication system files and directories"""
    if not os.path.exists(CHAT_HISTORY_DIR):
        os.makedirs(CHAT_HISTORY_DIR)

    if not os.path.exists(AUTH_FILE):
        with open(AUTH_FILE, 'w') as f:
            json.dump({"users": []}, f)

def hash_password(password):
    """Hash the password using the double SHA512 method"""
    h = hashlib.new('SHA512')
    h.update(password.encode())
    password = h.hexdigest()
    h.update(password.encode())
    return h.hexdigest()

def get_user_chat_history(username):
    """Get the chat history file path for a user"""
    return os.path.join(CHAT_HISTORY_DIR, f"{username}_history.txt")

def add_new_user(username, password):
    """Add a new user to the system"""
    initialize_auth_system()

    try:
        with open(AUTH_FILE, 'r') as file:
            auth_data = json.load(file)
    except FileNotFoundError:
        print("Password database not found!")
        sys.exit()

    # Check if username exists
    for user in auth_data['users']:
        if user['username'] == username:
            print("Username already exists!")
            return False

    # Add new user
    hashed_pw = hash_password(password)
    new_user = {
        "username": username,
        "password": hashed_pw
    }
    auth_data['users'].append(new_user)

    with open(AUTH_FILE, 'w') as f:
        json.dump(auth_data, f, indent=4)

    # Create empty chat history file
    with open(get_user_chat_history(username), 'w') as f:
        pass

    return True

username = enterbox("Create a username:", "Add new user")
password = passwordbox("Create a password:")
