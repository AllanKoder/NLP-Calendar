import os
from flask import Flask, render_template, request

#import the objects classes in the project directiory
from CommandInterpreter import CommandInterpreter

WordDictionary = CommandInterpreter()

app = Flask(__name__)
@app.route('/')
def Home():
    return render_template("home.html")

@app.route('/',methods=['POST'])
def multiply():
    if request.method == "POST":
        text = request.form['command']
        try:
            return f"<h1>definition is: {WordDictionary.define(text)}</h1>"
        except:
            return ""
        
@app.route('/<',methods=['GET','POST'])
def multiply():
    if request.method == "POST":
        text = request.form['command']
        try:
            return f"<h1>definition is: {WordDictionary.define(text)}</h1>"
        except:
            return ""
'''
@app.route("/predict", methods=['POST'])
def prediction():
'''
if __name__ == "__main__":
    app.run(debug=True)

