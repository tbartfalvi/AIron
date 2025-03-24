import bcrypt

def encrypt_password(password: str):
    salt = bcrypt.gensalt()
    # Hash the text with the salt
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def check_password(password: str, password_to_check: str):
    salt = bcrypt.gensalt()
    # hash first password
    hash = bcrypt.hashpw(password.encode('utf-8'), salt)
    # compare to the password_to_check
    return bcrypt.checkpw(password_to_check.encode('utf-8'), hash)