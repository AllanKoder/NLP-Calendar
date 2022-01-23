from flask import render_template, request, url_for, redirect, session, flash
from calendarweb import app 

#this is a cicrular dependency, the database needs to be imported before the app
from calendarweb.models import User, Event

from functools import wraps
#relational database
from calendarweb.forms import RegistrationForm, LoginForm
#import the objects classes in the project directiory
from calendarweb.Dictionary import Dictionary
from calendarweb.ContentCreator import ContentCreator
from calendarweb.LanguageParser import LanguageParser
from calendarweb.DateDataManager import DateDataManager

#create tword2number objects for the classes in the project directory 
WordDictionary = Dictionary()
CommandInterpreter = LanguageParser()
PostCreator = ContentCreator()
DataManager = DateDataManager()


default = [{
    'title': 'Input below or select a date',
}]

@app.route('/',methods=['POST', 'GET'])
def Home():
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
        elif request.form.get("date"):
            value = request.form['date']
            return redirect(url_for('viewdate',values=value))
        elif request.form.get("statistics"):
            return redirect(url_for('statistics'))
    return render_template("timeline.html", dates=default)

#Login required decorator
def loginRequired(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if "loggedIn" in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first", "danger")
            return redirect(url_for("Login"))
    return wrap

@app.route('/login', methods=['POST', 'GET'])
def Login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "admin@a.ca" and form.password.data == "admin":
            flash("You have been logged in!", "success")
            session["loggedIn"] = True
            return redirect(url_for("Home"))
        else:
            flash("Login Unsuccessful. Please check username and password", "danger")
    return render_template('login.html',form=form)

@app.route('/register', methods=['POST', 'GET'])
def Register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}', 'success')
        session["loggedIn"] = True
        return redirect(url_for('Home'))
    else:
        pass
    return render_template('register.html',form=form)

@app.route('/logout')
def Logout():
    session.pop("loggedIn", None)
    return redirect(url_for('Home', dates=default, message="You have been logged out"))
        
@app.route("/viewdate/<values>", methods=['GET', 'POST'])
@loginRequired
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
        elif request.form.get("date"):
            value = request.form['date']
            return redirect(url_for('viewdate',values=value))
        elif request.form.get("delete"):
            IDvalue = request.form['delete']
            DataManager.deleteData(values, IDvalue)
            #return str(DataManager.getWholeData())
            return redirect(url_for('viewdate',values=values))
        elif request.form.get("statistics"):
            return redirect(url_for('statistics'))
        
    date = DataManager.getDate(values)
    if date is None:
        date = default
    InputtedDate = values.split("-")
    dateTitle = PostCreator.createDate(int(InputtedDate[0]), InputtedDate[1], InputtedDate[2])
    
    
    return render_template("timeline.html", dates=date, dateTitle=dateTitle)

@app.route("/stats", methods=['GET', 'POST'])
@loginRequired
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
        elif request.form.get("date"):
            value = request.form['date']
            return redirect(url_for('viewdate',values=value))
    
    #get the hours from each activity using the data class
    ActivityMap = DataManager.findAmountOfEachActivityPerDay()
    li = round(ActivityMap.get("leisure"),2)
    wi = round(ActivityMap.get("work"),2)
    ei = round(ActivityMap.get("exercise"),2)
    ni = round(ActivityMap.get("natural"),2)
    
    #get the total amount of events per day
    Events = DataManager.findTotalEvents()
    TotalDays = DataManager.findTotalDays()
    if TotalDays == 0:
        TotalDays = 1
    EventsPerDay = round(Events / TotalDays)
    
    maxEvents = 0
    TimeMaxOverlap = "None"
    if DataManager.findTotalDays() != 0:
        try:
            #find the busiest time of the day 
            maxEvents, maxEventTime = DataManager.findBusiestTimeOfDay()  
            
            #convert the military time to standard time
            midday = "a.m."
            if maxEventTime > 1200:
                maxEventTime = maxEventTime - 1200
                midday = "p.m."
            #in the rare case that maxtme has a decimal place, we ignore it
            l = len(str(maxEventTime).split(".")[0])
            minutes = str(round(int(str(maxEventTime)[l-2:l])/100*60))
            if len(minutes) == 1:
                minutes = "0" + minutes
            hours = int(str(maxEventTime)[:l-2])
            TimeMaxOverlap = str(hours) + ":" + str(minutes) + " " + midday
        except:
            TimeMaxOverlap = "No Durational Events"
    #return all the data to the html page
    return render_template("stats.html", l=li,w=wi,e=ei,n=ni,Events=Events,EventsPerDay=EventsPerDay,maxEventTime=TimeMaxOverlap,maxEvents=maxEvents)