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
      result =self.mongo.users.find_one({"$and":[{"email":email }, {"password":password}]})
      print(result)
      if result :
            session["email"] = result["email"]
            session["name"] = result["name"]
            session["logged_in"] = True
            session["id"] = str(result["_id"])
            return True
      else:
            return False

    def insertfunc(self,data_dict):
        result = self.mongo.users.insert(data_dict)
        if result:
            return True
        else:
            return False

    def fetch_user(self, username):
        return self.mongo.users.find_one({"email":username})

    def update_profile(self,data_object,email):
        result = self.mongo.users.update_one({"email":email},{"$set":data_object})
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
   
    def team_update_members(self,team_id,email,name):
        return self.mongo.teams.update_one({"team_id":team_id},{"$push":{"email":email,"team_members":name}})
    def team_check(self,team_id):
         result = self.mongo.teams.find_one({"team_id":team_id})
         if len(result["team_members"]) < 4 and session["name"] not in result["team_members"]:
             return True
         else:
             return False

    def fetch_teams(self):
        return self.mongo.teams.find()
    
    def insert_projects(self,data_dict):
        return self.mongo.projects.insert(data_dict)
    def print_projects(self):
        return self.mongo.projects.find()
        
      
