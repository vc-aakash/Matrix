from cryptography.fernet import Fernet

def generate_key():
    key = Fernet.generate_key()
    with open("encryption_key.key", "wb") as key_file:
        key_file.write(key)
    print("Encryption key generated")

def load_key():
    try:
        with open("encryption_key.key", "rb") as key_file:
            return key_file.read()
    except FileNotFoundError:
        print("Key not found. Generate key")
        return None

def encrypt_message(message, key):
    fernet = Fernet(key)
    encrypted_message = fernet.encrypt(message.encode())
    return encrypted_message

def decrypt_message(message, key):
    fernet = Fernet(key)
    decrypted_message = fernet.decrypt(message).decode()
    return decrypted_message

if __name__ == "__main__":
    print("Encryption Agent")
    print("1. Generate Key")
    print("2. Encrypt Message")
    print("3. Decrypt Message")
    print("4. Exit")

    while True:
        choice = input("Choose an option:")

        if (choice == "1"):
            generate_key()
        elif (choice == "2"):
            key = load_key()
            if key:
                message = input("Enter message to encrypt: ")
                encrypted_message = encrypt_message(message, key)
                print(f"Encrypted message: {encrypted_message.decode()}")
        elif (choice == "3"):
            key = load_key()
            if key:
                message = input("Enter encrypted message: ")
                try:
                    decrypted_message = decrypt_message(message, key)
                    print(f"Decrypted message: {decrypted_message}")
                except Exception as e:
                    print(f"Decryption failed: {e}")
        elif (choice == "4"):
            break

        else:
            print("Invalid choice")