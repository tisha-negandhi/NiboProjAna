import hashlib
from flask import Flask
from flask import render_template,request
from flask_pymongo import PyMongo
import hashlib

app = Flask(__name__)
app.config.from_object("config.Config")

mongo = PyMongo(app)

from models import Users

user_object = Users()

@app.route("/forgot_pass")
def forgot_pass():
    if request.method=="POST":
        email = request.form["email"]
        # operation to sent email baout forgot password link to reset password

@app.route("/", methods = ["GET" , "POST"])
def signin():
    result = user_object.fetch_users()
    for x in result:
        print(x)
    if request.method == "POST":
        if request.form["section_name"] == "login_form":
            print("inside login form ")
            email = request.form["email"]
            password = request.form["password"]
            password = hashlib.md5(password.encode()).hexdigest()
            print(email, password)
        if request.form["section_name"] == "forgot_pass":
            print("inside forgot password")
            email = request.form["email"]
            print(email)
            # operation to sent email baout forgot password link to reset password
    return render_template('signin.html')

@app.route("/blank",  methods = ["GET" , "POST"] )
def blank():     
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
    return render_template('profile.html')

if __name__=='__main__':
    app.run(debug=True)
