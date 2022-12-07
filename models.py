from app import mongo,app
from flask import session
import os ,datetime

class Users:
    def __init__(self):
        self.mongo= mongo.db
    
    def logout(self):
        session.pop("email",None)
        session.pop("logged_in",None)
        session.pop("id",None)
        session.pop("name",None)
        session.pop("usertype",None)

    def signinfunc(self,email,password):
        result =self.mongo.users.find_one({"$and":[{"email":email }, {"password":password}]})
        print(result)
        if result :
            session["email"] = result["email"]
            session["logged_in"] = True
            session["usertype"] = result["usertype"]
            session["id"] = str(result["_id"])
            session["name"] = result["name"]
            return True
        else:
            return False

    def insertfunc(self,data_dict):
        result = self.mongo.users.insert(data_dict)
        if result:
            return True
        else:
            return False

    def fetch_user(self, email, usertype):
        return self.mongo[usertype].find_one({"email":email})

    def update_profile(self,data_object,email, usertype):
        result = self.mongo[usertype].update_one({"email":email},{"$set":data_object})
        if result:
            return True
        else:
            return False

    def insert_team(self,data_dict):
        return self.mongo.teams.insert(data_dict)
    
    def insert_user_type(self,data_dict, table_name):
        return self.mongo[table_name].insert(data_dict)
    
    
   
    def team_update_members(self,team_id,email,name):
        result = self.mongo.teams.find_one({"team_id":team_id})
        self.mongo.teams.update_one({"team_id":team_id},{"$push":{"team_members":{"email":email,"name":name}}})
        # temp_users = []
        # for x in result["team_members"]:
        #     temp_users.append(x["email"]) 

        # if len(result["team_members"]) < 4 and session["email"] not in temp_users:
        #     self.mongo.teams.update_one({"team_id":team_id},{"$push":{"team_members":{"email":email,"name":name}}})
        #     return True
        # else:
        #     return False

    def team_check(self,team_id):
        result = self.mongo.teams.find_one({"team_id":team_id})
        temp_users = []
        for x in result["team_members"]:
            temp_users.append(x["email"])

        if len(result["team_members"]) < 4 and session["email"] not in temp_users:
            return True
        else:
            return False

    def fetch_teams(self,email):
        if session["usertype"] == "teacher":
            return self.mongo.teams.find()
        else:
             return self.mongo.teams.find({"team_members.email":email})

    
    def insert_projects(self,data_dict):
        return self.mongo.projects.insert(data_dict)

    def print_projects(self,email):
        if session["usertype"] == "teacher":
            return self.mongo.projects.find()
        else:
            return self.mongo.projects.find({"team_members.email":email})


    def upload_files(self,each_file,teamdet,data_dict):
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        filename= str(datetime.datetime.utcnow())+ "." + each_file.filename.split(".")[1]
        file_path = os.path.join(app.config['UPLOAD_FOLDER'],each_file.filename)
        each_file.save(file_path)
         
        result =  self.mongo.projects.update({"team_id":data_dict["team_id"]},{"$push":{"file_link":file_path.split("\\")[1]}})
        return result
   
        
      
