import hashlib 
import os
from flask import Flask,flash  
from flask import render_template,request, url_for, redirect, session
from flask_pymongo import PyMongo
import hashlib
from functools import wraps
import random ,datetime
#from werkzeug import secure_filename


app = Flask(__name__)
app.config.from_object("config.Config")

mongo = PyMongo(app)
from models import Users
user_object= Users()

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session and session['logged_in']:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('signin'))
    return wrap
		
@app.route("/register_user",methods = ["GET" , "POST"])
def register_user():
    if request.method == "POST":
        if request.form["section_name"] == "reg_form":
            passed_object = {}
            passed_object["name"]=request.form["name"]
            passed_object["email"]=request.form["email"]
            passed_object["phone"]=request.form["phone"]
            passed_object["usertype"]=request.form["usertype"]
            passed_object["password"] = hashlib.md5(request.form["password"].encode()).hexdigest()
            print(passed_object)
            res = user_object.insertfunc(passed_object)

           
            result= user_object.insert_user_type(data_dict=passed_object, table_name = passed_object["usertype"])    
            if res:
                flash("registration successful")
                return redirect (url_for('signin'))
            else :
                return redirect (url_for('register_user'))           
     
    return render_template('register.html')

    


@app.route("/", methods = ["GET" , "POST"])
def signin():
    user_object.logout()
    if request.method == "POST":
        if request.form["section_name"] == "login_form":
            print("inside login form")
            email=request.form["email"]
            password=request.form["password"]
            password = hashlib.md5(password.encode()).hexdigest()
            result = user_object.signinfunc(email,password)
            if result:
               return redirect('/blank')
            else :
               return render_template("signin.html",context="Incorrect email or password")
        if request.form["section_name"] == "forgot_pass":
            print("inside forgot password")
            email=request.form["email"]
            print(email)

    return render_template('signin.html')

@app.route("/blank",  methods = ["GET" , "POST"] )
@login_required
def blank():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        password = hashlib.md5(password.encode()).hexdigest()
        
    return render_template('blank.html')

@app.route("/teampage", methods = ["GET" , "POST"]) 
@login_required
def teams():
    if request.method == "POST":
        if request.form["section_name"] == "create_team":
            print("inside create team")
            passed_object = {}
            
            for each in request.form:
              passed_object[each] = request.form[each]

            passed_object["team_leader"] = session["name"]
            passed_object["team_id"] = str(random.getrandbits(16))
            print(passed_object)
            user_object.insert_team(passed_object)
            user_object.team_update_members(email=session["email"],team_id=passed_object["team_id"],name=session["name"])
            return redirect(url_for('teams'))
           
        if request.form["section_name"] == "join_team":
            print("inside join team")
            team_id=request.form["team_id"]
            r = user_object.team_check(team_id=team_id)
            
            if r:
                user_object.team_update_members(email=session["email"],team_id=team_id,name=session["name"])
                return redirect (url_for('teams'))
            else:
                flash("u r already a member of this team or this team is full")
                return redirect (url_for('teams'))
    res = user_object.fetch_teams(email=session["email"])
    return render_template('team.html',context=res)

@app.route("/project", methods = ["GET" , "POST"])
@login_required
def project():
    result = user_object.print_projects(email=session["email"])
    return render_template('project.html',result=result)

@app.route("/projectform", methods = ["GET" , "POST"] )
@login_required
def projectform():
    if request.method == "POST":
        if request.form["section_name"] == "sub_proj":
            passed_object = {}
            teamdet = user_object.fetch_teams(email=session["email"])        
            for each in request.form:
                passed_object[each] = request.form[each]
            # passed_object["team_id"]= teamdet["team_id"]
            # passed_object["team_name"]= teamdet["team_name"]
            result1 = user_object.insert_projects(data_dict=passed_object)
            files = request.files.getlist("images")

            for each_file in files:
                result2=user_object.upload_files(each_file=each_file,teamdet=teamdet,data_dict= passed_object)
            
            if result1 and result2:
                return redirect('/project')
    return render_template('projectform.html')



@app.route("/profile", methods = ["GET" , "POST"]) 
@login_required
def profile():
    if request.method == "POST":
        passed_object = {}
        for each in request.form:
            passed_object[each] = request.form[each]
        user_object.update_profile(email=session["email"] ,data_object=passed_object, usertype = session["usertype"])
    user = user_object.fetch_user(email=session["email"],usertype = session["usertype"])
    return render_template('profile.html',users_context=user)
   
if __name__=='__main__':
    app.run(debug=True)
