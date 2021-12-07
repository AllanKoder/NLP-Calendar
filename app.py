import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from word2number import w2n
from datetime import datetime
#import the objects classes in the project directiory
from Dictionary import Dictionary
from LanguageParser import LanguageParser

app = Flask(__name__)
#location of the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dateEvents.db'
#intialize the database
db = SQLAlchemy(app)

#create the database 
class dates (db.Model):
    id = db.Column(db.Integer, primary_key=True);
    name = db.Column(db.String(20), nullable=False);
    date_created = db.Column(db.DateTime, default=datetime.utcnow);
    #create a function to return a string when we add something to the database
    def __represnt__(self):
        return '<Name: %r>' % self.id

#create tword2numberhe objects for the classes in the project directory 
WordDictionary = Dictionary()
CommandInterpreter = LanguageParser()


default = [
    {
        'title': 'waiting',
        'type': 'waiting',
        'time': "waiting",
        'tips': 'click on a day'
    }
]

@app.route('/')
def Home():
    return render_template("home.html", dates=default)

@app.route('/',methods=['POST', 'GET'])
def InputCommand():
    if request.method == "POST":
        if request.form.get("command"):
            text = request.form['command']
            try:
                return f"<h1>This is a: {CommandInterpreter.getSubject(text)}</h1>"
            except:
                return f"<h1>This is a: {CommandInterpreter.getSubject(text)}</h1>"
        if request.form.get("date"):
            value = request.form['date']
            return redirect(url_for('viewdate',values=value))

@app.route("/viewdate/<values>", methods=['GET', 'POST'])
def viewdate(values):
    dates = [
    {
        'title': values,
        'type': 'reminder',
        'time': "8:00am",
        'tips': 'remember to eat'
    }
    ]
    if request.method == "POST":
        if request.form.get("command"):
            text = request.form['command']
            try:
                return f"<h1>This is a: {CommandInterpreter.getSubject(text)}</h1>"
            except:
                return f"<h1>This is a: {w2n.word_to_num(text)}</h1>"
        if request.form.get("date"):
            value = request.form['date']
            return redirect(url_for('viewdate', values=value))

    return render_template("home.html", dates=dates)


if __name__ == "__main__":
    app.run(debug=True)

