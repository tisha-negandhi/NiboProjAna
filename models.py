from app import mongo
from flask import session

class Users:
    def __init__(self):
        self.mongo= mongo.db
    
    def logout(self):
        session.pop("email",None)
        session.pop("logged_in",None)
        session.pop("_id",None)

    def signinfunc(self,email,password):
      result =self.mongo.reg.find_one({"$and":[{"email":email }, {"password":password}]})
      print(result)
      if result :
            session["email"] = result["email"]
            session["logged_in"] = True
            session["id"] = str(result["_id"])
            return True
      else:
            return False

    def insertfunc(self,data_dict):
        return self.mongo.reg.insert(data_dict)

    def fetch_user(self, username):
        return self.mongo.reg.find_one({"email":username})

    def update_profile(self,data_object,email):
        result = self.mongo.reg.update_one({"email":email},{"$set":data_object})
        if result:
            return True
        else:
            return False

    def insert_team(self,data_dict):
        return self.mongo.teams.insert(data_dict)
    
    def insert_student(self,data_dict):
        return self.mongo.students.insert(data_dict)
    
    def insert_teacher(self,data_dict):
        return self.mongo.teachers.insert(data_dict)
   
    def team_update_members(self, full_name,team_id):
        result=self.mongo.teams.update_one({"team_id":team_id},{"$push":{"team_members":full_name}})
