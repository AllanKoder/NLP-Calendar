from LanguageParser import LanguageParser
lp = LanguageParser()
class ContentCreator:
    def __init__(self):
        self.title = "Empty"
        self.time = "1200"
        self.date = "12-0-0"
    def createPost(self, text):
        convertedNumberText = lp.wordToNumberSentence(lp.seperateTime(text)).lower()
        eventDate = lp.getEventDate(convertedNumberText)
        reminder_duration_class = lp.classify(convertedNumberText)
        eventStartTime = lp.getEventStartTime(convertedNumberText)
        subject = lp.getSubject(convertedNumberText)

        eventDuration = "0"
        if reminder_duration_class == "duration":
            eventDuration = lp.getEventDurationTime(convertedNumberText)

        
        output = [
            {
                'title': subject,
                'type': reminder_duration_class,
                'time': eventStartTime,
                'duration': eventDuration,
                'date': eventDate 
            }
        ]
        
        return output