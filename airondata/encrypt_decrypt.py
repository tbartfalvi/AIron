import bcrypt

def encrypt(text):
    salt = bcrypt.gensalt()

    # Hash the text with the salt
    return bcrypt.hashpw(text.encode('utf-8'), salt)
