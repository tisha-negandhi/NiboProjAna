import hashlib
from flask import Flask
from flask import render_template,request
import hashlib
app = Flask(__name__)

@app.route("/", methods = ["GET" , "POST"])
def signin():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        password = hashlib.md5(password.encode()).hexdigest()
     

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