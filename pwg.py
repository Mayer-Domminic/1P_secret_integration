import string
import secrets

def generate(length, use_digits, use_symbols, use_uppercase, use_lowercase):
    characters = ""
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_lowercase:
        characters += string.ascii_lowercase
    if use_digits:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    if len(characters) == 0:
        raise ValueError("At least one character type must be selected")

    # Generate a password by selecting randomly from the combined character set
    password = ''.join(secrets.choice(characters) for _ in range(length))

    return password

def password_gen(length, use_digits, use_symbols, use_uppercase, use_lowercase):
    try:
        password = generate(length, use_digits, use_symbols, use_uppercase, use_lowercase)
        return password
    except ValueError as e:
        print(f"Error: {e}")
