import sys
import hashlib
import os
import ollama
import json
from diffusers import StableDiffusionPipeline

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


def get_input(prompt, password=False):
    """Get user input with optional password masking"""
    if password:
        import getpass
        return getpass.getpass(prompt)
    return input(prompt)


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
        username = get_input("Enter username: ")
        if not username:
            continue

        entered_password = get_input("Enter password: ", password=True)
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


def display_chat_history(username):
    """Display the user's chat history"""
    history_file = get_user_chat_history(username)
    try:
        with open(history_file, "r") as f:
            print("\n--- Chat History ---")
            print(f.read())
            print("--------------------\n")
    except FileNotFoundError:
        print(f"\nNo chat history found for {username}\n")


def save_chat_message(username, message, sender="You"):
    """Save a message to the user's chat history"""
    history_file = get_user_chat_history(username)
    with open(history_file, "a") as f:
        f.write(f"{sender}: {message}\n")


def check_important_info():
    """Check and return important info"""
    try:
        with open("important_info.txt", "r", encoding="utf-8") as file:
            imp_info = file.read().replace("\n", " ")

        if "Remember, the developers of QRX3 Chatbot are Vedant. And you are QRX3 chatbot." not in imp_info:
            print("The required line is missing in 'important_info.txt'.")
            sys.exit()
        return imp_info
    except FileNotFoundError:
        print("The 'important_info.txt' file is missing.")
        sys.exit()


def generate_image(prompt, username):
    """Generate and save an image using Stable Diffusion"""
    print(f"Generating image for: {prompt}...")

    # Initialize Stable Diffusion
    pipe = StableDiffusionPipeline.from_pretrained("CompVis/stable-diffusion-v1-4")
    pipe.to("mps")

    image = pipe(prompt).images[0]
    file_path = f"generated_image_{username}.png"

    image = image.convert("RGB")
    image.save(file_path)
    print(f"Image saved as: {file_path}")


def chat_loop(username):
    """Main chat loop for the CLI interface"""
    print(f"\nWelcome to QRX3 Chatbot, {username}!")
    print("Type 'exit' to quit or 'image: your prompt' to generate an image\n")

    # Initialize Stable Diffusion pipe for faster subsequent image generation
    sd_pipe = None

    while True:
        user_input = get_input("You: ").strip()
        if not user_input:
            continue

        if user_input.lower() == 'exit':
            print("Goodbye!")
            break

        # Save user message
        save_chat_message(username, user_input)

        # Image generation
        if user_input.lower().startswith("image:"):
            prompt = user_input[6:].strip()
            generate_image(prompt, username)
            continue

        # Check important info
        imp_info = check_important_info()

        # Get chat history
        history_file = get_user_chat_history(username)
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

        # Display and save response
        print(f"QRX3: {reply}")
        save_chat_message(username, reply, "QRX3")


if __name__ == "__main__":
    # First-time setup check
    initialize_auth_system()

    with open(AUTH_FILE, 'r') as f:
        auth_data = json.load(f)

    if not auth_data['users']:
        print("No users found. Creating first user.")
        username = get_input("Create a username: ")
        if not username:
            sys.exit()

        password = get_input("Create a password: ", password=True)
        if not password:
            sys.exit()

        if add_new_user(username, password):
            print(f"User {username} created successfully!")
        else:
            sys.exit()

    # Normal authentication
    username = verify_password()
    if username:
        display_chat_history(username)
        chat_loop(username)