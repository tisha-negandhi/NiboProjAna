from app import mongo
from flask import session

class Users:
    def __init__(self):
        self.mongo = mongo.db
    
    def fetch_users(self):
        return self.mongo.users.find()