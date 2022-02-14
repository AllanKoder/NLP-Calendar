import bcrypt
from flask import render_template, request, url_for, redirect, session, flash
from calendarweb import app 
#this is a cicrular dependency, the database needs to be imported before the app
from calendarweb.models import User, Event
from calendarweb import db

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


defaultInformation = [{
    'title': 'Input below or select a date',
}]

@app.route('/',methods=['POST', 'GET'])
def Home():
    loggedIn = "loggedIn" in session
    username = session['username'] if loggedIn else None
    if request.method == "POST":
        if request.form.get("command"):
            if loggedIn:
                text = request.form['command']
                #get the command from the user and add to the database
                date = PostCreator.createPost(text)
                dateKey = CommandInterpreter.getEventDate(PostCreator.cleanText(text))
                DataManager.addData(date,session.get("emailID"))
                #get the date from the user and add to the database
                #return str(DataManager.getWholeData())
                return redirect(url_for('Viewdate',values=dateKey))
            else:
                flash("You need to login first", "danger")
                return redirect(url_for("Login"))
        elif request.form.get("date"):
            value = request.form['date']
            return redirect(url_for('Viewdate',values=value))
        elif request.form.get("Statistics"):
            return redirect(url_for('Statistics',username=username))         
    return render_template("timeline.html", dates=defaultInformation,username=username)

#Login required decorator, can be any parameter you want
def LoginRequired(f):
    #this would be the function that is being decorated 
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
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.checkpw(form.password.data.encode('utf-8') ,user.password):
            #add all the session cookies for the website data to load throughout pages
            session['loggedIn'] = True
            session["emailID"] = form.email.data
            session["username"] = User.query.filter_by(email=form.email.data).first().username
            flash(f"You are now logged in, {user.username}", "success")
            DataManager.setLocalData(session.get("emailID"))
            return redirect(url_for('Home',username=session.get("username")))
        else:
            flash("Login Unsuccessful. Please check username and password", "danger")
    return render_template('login.html',form=form)

@app.route('/register', methods=['POST', 'GET'])
def Register():
    form = RegistrationForm()
    if form.validate_on_submit():
        #hash the password and convert to a string 
        hashed_password = bcrypt.hashpw(str(form.password.data).encode('utf8'), bcrypt.gensalt())
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}', 'success')
        session["loggedIn"] = True
        session["emailID"] = form.email.data
        session["username"] = User.query.filter_by(email=form.email.data).first().username
        return redirect(url_for('Home',username=session.get("username")))
    else:
        pass
    return render_template('register.html',form=form)

@app.route('/logout')
def Logout():
    session.pop("loggedIn", None)
    session.pop("emailID", None)
    session.pop("username", None)
    flash('You have logged out!', 'success')
    return redirect(url_for('Home'))
        
@app.route("/Viewdate/<values>", methods=['GET', 'POST'])
@LoginRequired
def Viewdate(values):
    if request.method == "POST":
        if request.form.get("command"):
            text = request.form['command']
            
            date = PostCreator.createPost(text)
            dateKey = CommandInterpreter.getEventDate(PostCreator.cleanText(text))
            DataManager.addData(date, session.get("emailID"))
            InputtedDate = dateKey.split("-")
            dateTitle = PostCreator.createDate(int(InputtedDate[0]), InputtedDate[1], InputtedDate[2])
            return render_template("timeline.html", dates=DataManager.getDate(dateKey),dateTitle=dateTitle,username=session.get("username"))
        elif request.form.get("date"):
            value = request.form['date']
            return redirect(url_for('Viewdate',values=value,username=session.get("username")))
        elif request.form.get("delete"):
            IDvalue = request.form['delete']
            DataManager.deleteData(values, IDvalue, session.get("emailID"))
            #return str(DataManager.getWholeData())
            return redirect(url_for('Viewdate',values=values,username=session.get("username")))
        elif request.form.get("Statistics"):
            return redirect(url_for('Statistics',username=session.get("username")))
        
    date = DataManager.getDate(values)
    if date is None:
        date = defaultInformation
    InputtedDate = values.split("-")
    dateTitle = PostCreator.createDate(int(InputtedDate[0]), InputtedDate[1], InputtedDate[2])
    
    
    return render_template("timeline.html", dates=date, dateTitle=dateTitle,username=session.get("username"))

@app.route("/stats", methods=['GET', 'POST'])
@LoginRequired
def Statistics():
    if request.method == "POST":
        if request.form.get("command"):
            text = request.form['command']
            
            date = PostCreator.createPost(text)
            dateKey = CommandInterpreter.getEventDate(PostCreator.cleanText(text))
            DataManager.addData(date,session["usernameID"])
            InputtedDate = dateKey.split("-")
            dateTitle = PostCreator.createDate(int(InputtedDate[0]), InputtedDate[1], InputtedDate[2])
            return render_template("timeline.html", dates=DataManager.getDate(dateKey),dateTitle=dateTitle,username=session.get("username"))
        elif request.form.get("date"):
            value = request.form['date']
            return redirect(url_for('Viewdate',values=value,username=session.get("username")))
    
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