import os
from flask import Flask, render_template, request, url_for, redirect
#import the objects classes in the project directiory
from CommandInterpreter import CommandInterpreter

WordDictionary = CommandInterpreter()


default = [
    {
        'title': 'waiting',
        'type': 'waiting',
        'time': "waiting",
        'tips': 'click on a day'
    }
]

app = Flask(__name__)
@app.route('/')
def Home():
    return render_template("home.html", dates=default)

@app.route('/',methods=['POST', 'GET'])
def InputCommand():
    if request.method == "POST":
        if request.form.get("command"):
            text = request.form['command']
            try:
                return f"<h1>definition is: {WordDictionary.define(text)}</h1>"
            except:
                return ""
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
                return f"<h1>definition is: {WordDictionary.define(text)}</h1>"
            except:
                return ""
        if request.form.get("date"):
            value = request.form['date']
            return redirect(url_for('viewdate',values=value))

    return render_template("home.html", dates=dates)


if __name__ == "__main__":
    app.run(debug=True)

