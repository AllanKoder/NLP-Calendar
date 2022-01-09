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


default = [{
        'title': 'Input below or select a date',
}]

@app.route('/')
def Home():
    return render_template("timeline.html", dates=default)

@app.route('/',methods=['POST', 'GET'])
def InputCommand():
    if request.method == "POST":
        if request.form.get("command"):
            text = request.form['command']
            #get the command from the user and add to the database
            date = PostCreator.createPost(text)
            dateKey = CommandInterpreter.getEventDate(PostCreator.cleanText(text))
            DataManager.addData(date)
            #get the date from the user and add to the database
            #return str(DataManager.getWholeData())
            return redirect(url_for('viewdate',values=dateKey))
        if request.form.get("date"):
            value = request.form['date']
            return redirect(url_for('viewdate',values=value))
        if request.form.get("statistics"):
            return redirect(url_for('statistics'))
        
@app.route("/viewdate/<values>", methods=['GET', 'POST'])
def viewdate(values):
    if request.method == "POST":
        if request.form.get("command"):
            text = request.form['command']
            
            date = PostCreator.createPost(text)
            dateKey = CommandInterpreter.getEventDate(PostCreator.cleanText(text))
            DataManager.addData(date)
            InputtedDate = dateKey.split("-")
            dateTitle = PostCreator.createDate(int(InputtedDate[0]), InputtedDate[1], InputtedDate[2])
            return render_template("timeline.html", dates=DataManager.getDate(dateKey),dateTitle=dateTitle)
        if request.form.get("date"):
            value = request.form['date']
            return redirect(url_for('viewdate',values=value))
        if request.form.get("delete"):
            IDvalue = request.form['delete']
            DataManager.deleteData(values, IDvalue)
            #return str(DataManager.getWholeData())
            return redirect(url_for('viewdate',values=values))

    date = DataManager.getDate(values)
    if date is None:
        date = default
    InputtedDate = values.split("-")
    dateTitle = PostCreator.createDate(int(InputtedDate[0]), InputtedDate[1], InputtedDate[2])
    
    return render_template("timeline.html", dates=date, dateTitle=dateTitle)
@app.route("/stats", methods=['GET', 'POST'])
def statistics():
    if request.method == "POST":
        if request.form.get("command"):
            text = request.form['command']
            
            date = PostCreator.createPost(text)
            dateKey = CommandInterpreter.getEventDate(PostCreator.cleanText(text))
            DataManager.addData(date)
            InputtedDate = dateKey.split("-")
            dateTitle = PostCreator.createDate(int(InputtedDate[0]), InputtedDate[1], InputtedDate[2])
            return render_template("timeline.html", dates=DataManager.getDate(dateKey),dateTitle=dateTitle)
        if request.form.get("date"):
            value = request.form['date']
            return redirect(url_for('viewdate',values=value))
    return render_template("stats.html", l=10,w=12,e=12,n=1)
if __name__ == "__main__":
    app.run(debug=True)