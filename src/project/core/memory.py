# Simple memory store (TinyDB stub)
from tinydb import TinyDB

db = TinyDB('data/memory.json')

def log(entry):
    db.insert(entry)

def fetch_all():
    return db.all()
