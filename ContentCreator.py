from LanguageParser import LanguageParser
from DateDataManager import DateDataManager
import random 
lp = LanguageParser()
dm = DateDataManager()
class ContentCreator:
    def __init__(self):
        self.cleanedText = ""
        self.eventDate = ""
        self.reminderDurationClass = ""
        self.eventStartTime = ""
        self.eventDuration = 0
        self.subject = ""
        self.activityClass = ""
    def cleanText(self, text):
        return lp.wordToNumberSentence(lp.seperateTime(text)).lower()
    def createPost(self, text):
        #Get the language of the text and place it into an object for the HTML 
        self.cleanedText = self.cleanText(text)
        uncaptilizedSubject = lp.getSubject(self.cleanedText)
        self.subject = lp.CapitalizeTitle(uncaptilizedSubject)
        self.eventDate = lp.getEventDate(self.cleanedText)
        self.reminderDurationClass = lp.classifyActivity(self.cleanedText,["Reminder","Duration"])
        eventTime = lp.getEventStartTime(self.cleanedText)
        self.eventStartTime = eventTime if eventTime != 0 else None
        eventDuration = lp.getEventDurationTime(self.cleanedText)

        self.activityClass =  lp.classifyActivity(uncaptilizedSubject, ["Leisure", "Work", "Exercise", "Natural"])
        
        self.eventDuration = 0     
        if self.reminderDurationClass == "duration" or eventDuration != None:
            self.reminderDurationClass = "duration"
            self.eventDuration = eventDuration
            if self.eventDuration == None:
                self.eventDuration = 60
        
        splitDate = self.eventDate.split("-")
        dateInput = self.createDate(int(splitDate[0]), splitDate[1], splitDate[2])
        randomColor = self.createColor()
        while dm.colorUsed(dateInput,randomColor):
            randomColor = self.createColor()
        
        output = {
                'title': self.subject,
                'type': self.reminderDurationClass,
                'time': self.eventStartTime,
                'duration': self.eventDuration,
                'date': self.eventDate,
                'color': randomColor,
                'class': self.activityClass,
                }   

        return output
    def createDate(self, month, day, year):
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        return months[month] + " " + day + ", " + year
    def createColor(self):
        return "rgb(" + str(random.randint(30,140)) + "," + str(random.randint(30,140)) + "," + str(random.randint(30,140)) + "," + str(0.7) + ")"