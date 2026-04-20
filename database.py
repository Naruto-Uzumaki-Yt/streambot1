from pymongo import MongoClient
from config import DB_URL

client = MongoClient(DB_URL)
db = client["streambot"]
col = db["files"]

def save_file(file_id, name, size, mime):
    return col.insert_one({
        "file_id": file_id,
        "name": name,
        "size": size,
        "mime": mime
    }).inserted_id

def get_file(_id):
    return col.find_one({"_id": _id})
