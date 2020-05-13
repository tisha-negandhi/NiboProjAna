from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route("/")
def signin():
    return render_template('signin.html')

@app.route("/blank")
def blank():
    return render_template('blank.html')

@app.route("/teampage")
def teams():
    return render_template('team.html')

@app.route("/project")
def proeject():
    return render_template('project.html')

@app.route("/projectform")
def proejectform():
    return render_template('projectform.html')

@app.route("/profile")
def sam():
    return render_template('profile.html')

if __name__=='__main__':
    app.run(debug=True)