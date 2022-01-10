from flask import Flask, render_template, request, url_for, redirect
#import the objects classes in the project directiory
from Dictionary import Dictionary
from ContentCreator import ContentCreator
from LanguageParser import LanguageParser
from DateDataManager import DateDataManager

app = Flask(__name__)

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
        elif request.form.get("date"):
            value = request.form['date']
            return redirect(url_for('viewdate',values=value))
        elif request.form.get("statistics"):
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
    l = round(ActivityMap.get("leisure"),3)
    w = round(ActivityMap.get("work"),3)
    e = round(ActivityMap.get("exercise"),3)
    n = round(ActivityMap.get("natural"),3)

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
            TimeMaxOverlap = "All events have been deleted"
    #return all the data to the html page
    return render_template("stats.html", l=l,w=w,e=e,n=n,Events=Events,EventsPerDay=EventsPerDay,maxEventTime=TimeMaxOverlap,maxEvents=maxEvents)
if __name__ == "__main__":
    app.run(debug=True)