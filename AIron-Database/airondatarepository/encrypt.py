import bcrypt

def encrypt_password(password: str):
    salt = bcrypt.gensalt()
    # Hash the text with the salt
    hashed_passsword = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_passsword.decode('utf-8')

def check_password(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))