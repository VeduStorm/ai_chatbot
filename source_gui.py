import sys
import hashlib
import os
import ollama
import json
from diffusers import StableDiffusionPipeline
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit,
    QPushButton, QLabel, QHBoxLayout
)
from PyQt5.QtCore import QTimer
from easygui import passwordbox, enterbox
from PyQt5.QtGui import QPixmap

# Constants
AUTH_FILE = 'auth.json'
main_gui = 'main_gui.py'
main_cli = 'main_cli.py'
CHAT_HISTORY_DIR = 'chat_histories'


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


def verify_password():
    """Verify user credentials with username support"""
    initialize_auth_system()

    try:
        with open(AUTH_FILE, 'r') as file:
            auth_data = json.load(file)
    except FileNotFoundError:
        print("Password database not found!")
        sys.exit()

    for attempt in range(3):
        username = enterbox("Enter username:", "Authentication")
        if not username:
            continue

        entered_password = passwordbox("Enter password:")
        if not entered_password:
            continue

        # Find user in auth data
        user = None
        for u in auth_data['users']:
            if u['username'] == username:
                user = u
                break

        if not user:
            print("User not found!")
            if attempt < 2:
                print("Try Again!")
                continue
            else:
                print("Access Denied!")
                os.remove(AUTH_FILE)
                os.remove(main_cli)
                os.remove(main_gui)
                sys.exit()

        # Verify password
        h = hashlib.new('SHA512')
        h.update(entered_password.encode())
        hashed_input = h.hexdigest()
        h.update(hashed_input.encode())
        final_hash = h.hexdigest()

        if final_hash == user['password']:
            return username  # Return username for session
        elif attempt < 2:
            print("Try Again! Wrong password.")
        else:
            print("Access Denied!")
            sys.exit()

    return None


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


class ChatbotGUI(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle(f"QRX3 AI Chatbot - {username}")
        self.setGeometry(100, 100, 600, 600)
        layout = QVBoxLayout()

        # Chat Display
        self.chat_history = QTextEdit(self)
        self.chat_history.setReadOnly(True)
        layout.addWidget(self.chat_history)

        # Image Display
        self.image_label = QLabel(self)
        layout.addWidget(self.image_label)

        # Input Layout
        input_layout = QHBoxLayout()

        # User Input
        self.entry = QLineEdit(self)
        self.entry.setPlaceholderText("Type a message...")
        self.entry.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.entry)

        # Send Button
        self.send_button = QPushButton("Send", self)
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)

        layout.addLayout(input_layout)
        self.setLayout(layout)
        self.load_chat_history()

        # Initialize Stable Diffusion
        self.sd_pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4")
        self.sd_pipe.to("mps")

    def load_chat_history(self):
        """Load the user's specific chat history"""
        history_file = get_user_chat_history(self.username)
        try:
            with open(history_file, "r") as f:
                self.chat_history.setText(f.read())
        except FileNotFoundError:
            self.chat_history.setText(f"Welcome {self.username}! Your chat history will appear here.")

    def save_chat_history(self):
        """Save the chat history to the user's specific file"""
        history_file = get_user_chat_history(self.username)
        with open(history_file, "w") as f:
            f.write(self.chat_history.toPlainText())

    def send_message(self):
        user_input = self.entry.text().strip()
        if not user_input:
            return

        # Check important info
        try:
            with open("important_info.txt", "r", encoding="utf-8") as file:
                imp_info = file.read().replace("\n", " ")

            if "Remember, the developers of QRX3 Chatbot are Vedant. And you are QRX3 chatbot." not in imp_info:
                print("The required line is missing in 'important_info.txt'.")
                sys.exit()
        except FileNotFoundError:
            imp_info = "No important information available."
            print("The 'important_info.txt' file is missing.")
            sys.exit()

        self.chat_history.append(f"<b>You:</b> {user_input}")
        self.save_chat_history()

        # Image generation
        if user_input.lower().startswith("image:"):
            prompt = user_input[6:].strip()
            self.generate_image(prompt)
        else:
            # Read user's specific chat history
            history_file = get_user_chat_history(self.username)
            try:
                with open(history_file, "r", encoding="utf-8") as file:
                    chat_history = file.read().replace("\n", " ")
            except FileNotFoundError:
                chat_history = "No chat history available."

            # Get response from chatbot
            try:
                response = ollama.chat(model="Vedu/QRX3_chatbot", messages=[
                    {"role": "system",
                     "content": f"{chat_history} This is our chat history, and now I'm going to provide some important information about my background: {imp_info}"},
                    {"role": "user", "content": user_input}
                ])
                reply = response['message']['content']
            except Exception as e:
                reply = f"Error: {e}"

            self.chat_history.append(f"<b>QRX3:</b> {reply}\n")
            self.save_chat_history()

        self.entry.clear()

    def generate_image(self, prompt):
        self.chat_history.append(f"Generating image for: {prompt} ...")
        self.save_chat_history()

        image = self.sd_pipe(prompt).images[0]
        file_path = f"generated_image_{self.username}.png"

        image = image.convert("RGB")
        image.save(file_path)
        print(f"Image saved at: {file_path}")

        pixmap = QPixmap(file_path)
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)
        QTimer.singleShot(10000, self.clear_image)

    def clear_image(self):
        self.image_label.clear()


if __name__ == "__main__":
    # First-time setup check
    initialize_auth_system()

    with open(AUTH_FILE, 'r') as f:
        auth_data = json.load(f)

    if not auth_data['users']:
        print("No users found. Creating first user.")
        username = enterbox("Create a username:", "First-time Setup")
        if not username:
            sys.exit()

        password = passwordbox("Create a password:")
        if not password:
            sys.exit()

        if add_new_user(username, password):
            print(f"User {username} created successfully!")
        else:
            sys.exit()

    # Normal authentication
    username = verify_password()
    if username:
        app = QApplication(sys.argv)
        chatbot = ChatbotGUI(username)
        chatbot.show()
        sys.exit(app.exec_())