from app import mongo
from flask import session

class Users:
    def __init__(self):
        self.mongo = mongo.db
    
    def signin_user(self,email,password):
        login_result = self.mongo.users.find_one({"$and":[{"email": email},{"password": password}]})
        if login_result:
            session["email"] = login_result["email"]
            session["logged_in"] = True
            session["id"] = str(login_result["_id"])
            return True
        else:
            return False
    
    def insert_user(self,data_object):
        return self.mongo.users.insert(data_object)

    def fetch_user(self, username):
        return self.mongo.users.find_one({"email":username})

    def update_profile(self,data_object,email):
        result = self.mongo.users.update_one({"email":email},{"$set":data_object})
        if result:
            return True
        else:
            return False
