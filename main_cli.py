from cryptography.fernet import Fernet
import tempfile
import os
import sys

KEY = os.environ.get('FERNET_KEY')
if not KEY:
        print("Error: FERNET_KEY environment variable not set!")
        with open('secrets', 'rb') as f:
            KEY = f.read()
        sys.exit(1)


def main():
    # Read the encrypted file
    encrypted_file = 'encrypted_cli'

    try:
        with open(encrypted_file, 'rb') as f:
            encrypted_data = f.read()
    except FileNotFoundError:
        print(f"Error: Encrypted file '{encrypted_file}' not found!")
        sys.exit(1)

    # Decrypt the file
    try:
        fernet = Fernet(KEY)
        decrypted_data = fernet.decrypt(encrypted_data)
    except Exception as e:
        print("Decryption failed:", str(e))
        sys.exit(1)

    # Create a temporary file
    try:
        with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as tmp:
            tmp.write(decrypted_data)
            tmp_path = tmp.name
    except Exception as e:
        print("Failed to create temporary file:", str(e))
        sys.exit(1)

    # Execute the decrypted script
    try:
        os.system(f'python3 "{tmp_path}"')
    finally:
        # Clean up - remove the temporary file
        try:
            os.unlink(tmp_path)
        except:
            pass


if __name__ == "__main__":
    main()