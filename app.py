import hashlib
from flask import Flask,flash
from flask import render_template,request, url_for, redirect, session
from flask_pymongo import PyMongo
import hashlib
from functools import wraps



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
		
@app.route("/register_user")
def register_user():
    pass_dict={}
    pass_dict["name"]="Tisha"
    pass_dict["email"]="tishanegandhi27@gmail.com"
    pass_dict["password"] = "12345"
    pass_dict["password"] = hashlib.md5(pass_dict["password"].encode()).hexdigest()
    result= user_object.insertfunc(pass_dict)
    if result:
        return "Inserted"
    else :
        return "Failure"





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
               return render_template("signin.html",message="Password Galat hai")
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
            print(passed_object)
            result= user_object.insert_team(passed_object)
            team_id=request.form["team_id"]
            full_name=request.form["team_leader"]
            result1=user_object.team_update_members(full_name=full_name,team_id=team_id)
           
        if request.form["section_name"] == "join_team":
            print("inside join team")
            team_id=request.form["team_id"]
            full_name=request.form["full_name"]
            result1=user_object.team_update_members(full_name=full_name,team_id=team_id)
    return render_template('team.html')

@app.route("/project", methods = ["GET" , "POST"])
@login_required
def project():
    if request.method == "POST":
        passed_object = {}
        for each in request.form:
            passed_object[each] = request.form[each]
       
    return render_template('project.html')

@app.route("/projectform", methods = ["GET" , "POST"] )
@login_required
def projectform():
    if request.method == "POST":
        passed_object = {}
        for each in request.form:
            passed_object[each] = request.form[each]
       
    return render_template('projectform.html')

@app.route("/profile", methods = ["GET" , "POST"]) 
@login_required
def profile():
    if request.method == "POST":
        passed_object = {}
        for each in request.form:
            passed_object[each] = request.form[each]
        result=user_object.update_profile(email=session["email"] ,data_object=passed_object)
    user = user_object.fetch_user(username=session["email"])
    return render_template('profile.html',users_context=user)
   
if __name__=='__main__':
    app.run(debug=True)