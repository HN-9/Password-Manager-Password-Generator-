import random
import string

def generate_password(length=16, numbers=True, symbols=True):
    chars = string.ascii_letters
    if numbers:
        chars += string.digits
    if symbols:
        chars += "!@#$%^&*()-_=+[]{};:,.<>?"

    return "".join(random.choice(chars) for _ in range(length))
