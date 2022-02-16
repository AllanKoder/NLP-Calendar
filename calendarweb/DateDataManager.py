from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from calendarweb import db
from calendarweb.models import User, Event 
class DateDataManager():
    def __init__(self):
        self.dateData = {}
        self.colorData = {}
    def addData(self, post, emailID):
        #add a post to the database using the date as the key and the post as the value, if the date does not exist, create it
        keyResult = self.dateData.get(post.get("date"))
        if keyResult is not None:
            keyResult.append(post)
            self.colorData[post.get("date")][post.get("color")] = True
        else:   
            #add a new date to the database
            self.dateData[post.get("date")] = [post]
            self.colorData[post.get("date")] = {post.get("color"):True}
        #get the id for the user by their unique username 
        userID = User.query.filter_by(email=emailID).first().id
        event = Event(userID=userID, title=post.get("title"), type=post.get("type"), date=post.get("date"), time=post.get("time"), duration=post.get("duration"), activityClass=post.get("class"), color=post.get("color"))
        #add the data to the database and assign a specific key to the user id
        db.session.add(event)
        db.session.commit()
    def setLocalData(self, emailID):
        userID = User.query.filter_by(email=emailID).first().id
        eventsData = Event.query.filter_by(userID=userID).all()
        #make the master dictionary for the date data        
        for event in eventsData:
            eventData = {
                "title": event.title,
                "type": event.type,
                "time": event.time,
                "duration": event.duration,
                "date": event.date,
                "color": event.color,
                "class": event.activityClass
            }
            if self.dateData.get(event.date) is None:
                self.dateData[event.date] = [eventData]
            else:
                self.dateData[event.date].append(eventData)
            if self.colorData.get(event.date) is None:
                self.colorData[event.date] = {event.color:True}
            else:
                self.colorData[event.date][event.color] = True
    def getDate(self, date):
        return self.dateData.get(date)
    def deleteData(self, date, ID, emailID):
        #delete a post from the database using the unique color as the ID and the date as the key
        listOfEvents = self.dateData.get(date)
        if listOfEvents is not None:
            for i in listOfEvents:
                if i.get("color") == ID:
                    listOfEvents.remove(i)
                    break
            userID = User.query.filter_by(email=emailID).first().id  
            deleteEvent = Event.query.filter_by(userID=userID, date=date, color=ID).first()
            db.session.delete(deleteEvent)
            db.session.commit()
            self.colorData[date][ID] = False
                
    def colorUsed(self, date, color):
        #check if a color is used in a date
        if self.colorData.get(date) == None:
            return False
        return self.colorData.get(date).get(color)
    def getWholeData(self):
        #return the entire database for testing purposes
        return str(self.dateData) + str(self.colorData)
    def findTotalEvents(self):
        # find the total amount of events in the database
        total = 0
        for i in self.dateData:
            total += len(self.dateData[i])
        return total
    def findAmountOfEachActivityPerDay(self):
        #find the amount of each activity in the database  
        #return a dictionary with the activity as the key and the amount as the value
        totalTimes = {"leisure":0, "work":0, "natural":0, "exercise":0}
        amountOfDays = len(self.dateData)
        if amountOfDays == 0:
            amountOfDays = 1
        for i in self.dateData:
            for j in self.dateData[i]:
                if j.get("class"):
                    totalTimes[j.get("class")] += j.get("duration")/60 
        
        #find the average amount of each activity per day
        for k in totalTimes:
            totalTimes[k] = totalTimes[k]/amountOfDays

        return totalTimes
    def findTotalEvents(self):
        #find the total amount of events in the database
        total = 0
        for i in self.dateData:
            total += len(self.dateData[i])
        return total
    def findTotalDays(self):
        #find the total amount of days in the database
        return len(self.dateData)
    def findBusiestTimeOfDay(self):
        #use a maximum overlap algorithm to find the busiest time of day
        arrivals, leaves = self.returnArrivalLeaveTimes()
        #use merge sort to sort the arrival and leave times
        arrivals.sort()
        leaves.sort()
        
        n = len(arrivals)


        events = 1
        maxEvents = 1
        #the starting time is the first arrival time
        time = arrivals[0]
        i = 1
        j = 0
        
        while (i < n and j < n):
            #upon finding a new arrival time, increment the events
            #upon finding a new leave time, decrement the events
            #if the events is greater than the max events, update the max events
            if (arrivals[i] <= leaves[j]):
                events = events + 1
                if(events > maxEvents):
                    maxEvents = events
                    time = arrivals[i]                
                i = i + 1; 
            else:
                events -= 1
                j = j + 1
        
        return maxEvents, time
        
    def returnArrivalLeaveTimes(self):
        arrivals = []
        leaves = []
        #find the arrival and leave times for each event and add them to the arrival and leave lists as long as the value is not zero
        for i in self.dateData:
            for j in self.dateData[i]:
                if int(j.get("time")) != 0:
                    arrivals.append(int(j.get("time")))
                    leaves.append(int(j.get("time")) + int(j.get("duration"))/60*100)
        return arrivals, leaves