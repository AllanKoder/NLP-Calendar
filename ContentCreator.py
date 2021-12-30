from LanguageParser import LanguageParser
import random 
lp = LanguageParser()
class ContentCreator:
    def __init__(self):
        self.cleanedText = ""
        self.eventDate = ""
        self.reminderDurationClass = ""
        self.eventStartTime = ""
        self.eventDuration = ""
        self.subject = ""
    def cleanText(self, text):
        return lp.wordToNumberSentence(lp.seperateTime(text)).lower()
    def createPost(self, text):
        #Get the language of the text and place it into an object for the HTML 
        self.cleanedText = self.cleanText(text)
        self.eventDate = lp.getEventDate(self.cleanedText)
        self.reminderDurationClass = lp.classify(self.cleanedText)
        self.eventStartTime = lp.getEventStartTime(self.cleanedText)
        self.subject = lp.getSubject(self.cleanedText)

        self.eventDuration = "0"
        if self.reminderDurationClass == "duration":
            self.eventDuration = lp.getEventDurationTime(self.cleanedText)

        randomColor = "rgb(" + str(random.randint(30,140)) + "," + str(random.randint(30,140)) + "," + str(random.randint(30,140)) + "," + str(0.7) + ")"
        output = {
                'title': self.subject,
                'type': self.reminderDurationClass,
                'time': self.eventStartTime,
                'duration': self.eventDuration,
                'date': self.eventDate,
                'message': "Successfully created event",
                'color': randomColor,
                }

        return output
    def createDate(self, month, day, year):
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        return months[month] + " " + day + ", " + year