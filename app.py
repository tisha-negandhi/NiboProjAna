from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route("/")
def deshna():
    return render_template('blank.html')

@app.route("/teampage")
def teams():
    return render_template('team.html')

if __name__=='__main__':
    app.run(debug=True)