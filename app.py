import os
from flask import Flask, render_template, request

#import the objects from the classes folder in the project directiory
from CommandInterpreter import CommandInterpreter

app = Flask(__name__)
@app.route('/')
def Home():
    return render_template("home.html")

@app.route('/',methods=['POST'])
def multiply():
    if request.method == "POST":
        number1 = request.form['text1']
        try:
            return f"<h1>product is: {float(number1)}</h1>"
        except:
            return ""
'''
@app.route("/predict", methods=['POST'])
def prediction():
'''
if __name__ == "__main__":
    app.run(debug=True)

