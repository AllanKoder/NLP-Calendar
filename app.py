import os
from re import I
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from word2number import w2n
from datetime import datetime
#import the objects classes in the project directiory
from Dictionary import Dictionary
from ContentCreator import ContentCreator
from LanguageParser import LanguageParser
from DateDataManager import DateDataManager

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
PostCreator = ContentCreator()
DataManager = DateDataManager()


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
                date = PostCreator.createPost(text)
                DataManager.addData(date)
                return render_template("home.html", dates=date)
            except:
                date = PostCreator.createPost(text)
                DataManager.addData(date)
                return render_template("home.html", dates=date)
        if request.form.get("date"):
            value = request.form['date']
            return redirect(url_for('viewdate',values=value))

@app.route("/viewdate/<values>", methods=['GET', 'POST'])
def viewdate(values):
    if request.method == "POST":
        if request.form.get("command"):
            text = request.form['command']
            try:
                date = PostCreator.createPost(text)
                return render_template("home.html", dates=date)
            except:
                date = PostCreator.createPost(text)
                DataManager.addData(date)
                return render_template("home.html", dates=date)
        if request.form.get("date"):
            value = request.form['date']
            return redirect(url_for('viewdate',values=value))

    
    date = DataManager.getDate(values)
    if date is None:
        date = default
    return render_template("home.html", dates=date)

if __name__ == "__main__":
    app.run(debug=True)

