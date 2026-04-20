import hashlib
from config import SECRET_KEY

def generate_hash(file_id):
    return hashlib.md5(f"{file_id}{SECRET_KEY}".encode()).hexdigest()

def verify_hash(file_id, h):
    if not h:
        return False
    return generate_hash(file_id) == h
