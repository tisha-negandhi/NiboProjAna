from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route("/")
def blank():
    return render_template('blank.html')

@app.route("/teampage")
def teams():
    return render_template('team.html')

<<<<<<< HEAD
@app.route("/project")
def project():
    return render_template('project.html')
=======
@app.route("/profile")
def sam():
    return render_template('profile.html')
>>>>>>> 0988a3335f9ad157ace27fd33a59870ea2564fd0

if __name__=='__main__':
    app.run(debug=True)