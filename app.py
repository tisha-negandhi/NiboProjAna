import hashlib
from flask import Flask
from flask import render_template,request,url_for,redirect,session
import hashlib
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config.from_object("config.Config")

mongo = PyMongo(app)
from models import Users
users_object =  Users()

@app.route("/register_user")
def register_user():
    pass_object = {}
    pass_object["full_name"] = "John Doe"
    pass_object["email"] = "johndoe@gmail.com"
    pass_object["password"] = "12345"
    pass_object["password"] = hashlib.md5(pass_object["password"].encode()).hexdigest()
    result = users_object.insert_user(data_object=pass_object)
    if result:
        return "inserted in databse"
    else:
        return "failed to insert"


@app.route("/", methods = ["GET" , "POST"])
def signin():
    
    if request.method == "POST":
        if request.form["section_name"] == "login_form":
            email = request.form["email"]
            password = request.form["password"]
            password = hashlib.md5(password.encode()).hexdigest()
            result = users_object.signin_user(email,password)
            if result:
                return redirect("/blank")
            else:
                return render_template("signin.html",context="email id and password does not match")
        if request.form["section_name"] == "forgot_pass":
             email = request.form["email"] 
    return render_template('signin.html')

@app.route("/blank",  methods = ["GET" , "POST"] )
def blank():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        password = hashlib.md5(password.encode()).hexdigest()
     
    return render_template('blank.html')

@app.route("/teampage", methods = ["GET" , "POST"]) 
def teams():
    if request.method == "POST":
        passed_object = {}
        for each in request.form:
            passed_object[each] = request.form[each]
        print(passed_object)
       
    return render_template('team.html')

@app.route("/project", methods = ["GET" , "POST"])
def project():
    if request.method == "POST":
        passed_object = {}
        for each in request.form:
            passed_object[each] = request.form[each]
       
    return render_template('project.html')

@app.route("/projectform", methods = ["GET" , "POST"] )
def projectform():
    if request.method == "POST":
        passed_object = {}
        for each in request.form:
            passed_object[each] = request.form[each]
       
    return render_template('projectform.html')

@app.route("/profile", methods = ["GET" , "POST"]) 
def profile():
    if request.method == "POST":
        passed_object = {}
        for each in request.form:
            passed_object[each] = request.form[each]
        result=users_object.update_profile(email=session["email"] ,data_object=passed_object)
    user = users_object.fetch_user(username=session["email"])
    return render_template('profile.html',users_context=user)

if __name__=='__main__':
    app.run(debug=True)