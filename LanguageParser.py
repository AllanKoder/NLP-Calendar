from io import StringIO
import pandas as pd
import numpy as np
import datetime
from word2number import w2n
import re
from stopwords import commandstopwords, stopwords, subjectstopwords
from Dictionary import Dictionary
WordDictionary = Dictionary()

class LanguageParser:
    #algorithm order: remove all the weird punctuation, filter the numbers, time, classify the command, filter the stopwords, filter the words, filter the words in the dictionary
    def classify(self, text):
        data = pd.read_csv("KeyWordsData.csv")
        data = data[data[['Duration','Reminder']].notna()]
        data[['Duration','Reminder']]=data[['Duration','Reminder']].astype(str)

        ReminderKeyWords = [x.lower().replace(" ", "") for x in data['Reminder'].tolist()]
        DurationKeyWords = [x.lower().replace(" ", "") for x in data['Duration'].tolist()]

        command_stop_words = set(commandstopwords.getwords())
        stop_words = set(stopwords.getwords())

        ReminderScore = 0
        DurationScore = 0

        filtered_sentence = []
        definitions = []
        BagOfWordsInput = []

        ReminderWordMap = {}
        DurationWordMap = {}


        for w in text.split(" "):
            if w.lower() not in command_stop_words:
                filtered_sentence.append(w)

        #use the dynamic bag of words to find the keywords
        for w in ReminderKeyWords:
            ReminderWordMap[w] = 1
        for w in DurationKeyWords:
            DurationWordMap[w] = 1


        for w in filtered_sentence:
            WordDefinition = WordDictionary.define(w)
            for key in WordDefinition:
                if isinstance(WordDefinition, dict):
                    for d in WordDefinition[key]:
                        definitions.append(d)
        totalwords = ""
        for s in definitions:
            totalwords += s + " "
        for s in filtered_sentence:
            totalwords += s + " "
        for w in totalwords.split(" "):
            if w.lower() not in stop_words:
                BagOfWordsInput.append(re.sub('[^a-zA-Z]+', '', w.lower()))

        for b in BagOfWordsInput:
            if ReminderWordMap.get(b):
                ReminderScore += 1
        for b in BagOfWordsInput:
            if DurationWordMap.get(b):
                DurationScore += 1
        returnoutput = "reminder" if ReminderScore >= DurationScore else "duration"
        return returnoutput
    def wordToNumber(self, text):
        try:
            return str(w2n.word_to_num(text))
        except:
            return None
    def wordToNumberSentence(self, text):
        textArray = text.split(" ")
        index = 0
        output = " "
        #get all the words that are numbers and convert it to a number in digit form
        while (index < len(textArray)):
            if self.wordToNumber(textArray[index]):
                additionalString = textArray[index] + " " 
                for j in range(index+1, len(textArray)):
                    if (self.wordToNumber(textArray[j])):
                        additionalString += textArray[j] + " "
                        index+=1
                    else:
                        break
                if self.wordToNumber(additionalString) != None:
                    output += self.wordToNumber(additionalString) + " "
                else:
                    output += textArray[index] + " "
            else:
                output += textArray[index] + " "
            index += 1
        return output
    def seperateTime(self,text):
        ctext = text
        index = 0
        #iterate all the characters in text 
        for ind,cha in enumerate(ctext):
            v = ind + index
            #if the character is a number, and the next character is not a number, then it is a time, and we want to seperate it
            if cha.isdigit() and v+1 < len(text):
                if text[v+1].isdigit() == False and text[v+1] != " ":
                    text = text[:v+1] + " " + text[v+1:]   
                    index += 1
        return text
    def getEventStartTime(self, text):
        #if there is the word 'at' inside the text, find the time that accomadates it: 
        textA = text.split(" ")
        time = None
        Periodindex = 0
        keywords = ["at", "after"]
        periodKeywords = ["in", "on"]
        nonPeriodDictionary = {"morning": "900", "afternoon": "1200", "evening": "1800", "night": "2100","midnight": "0000", "noon": "1200", "midday": "1200","breakfast": "900", "lunch": "1200", "dinner": "1800"}
        for v,a in enumerate(textA): 
            #turning time into military clock time 
            if a in keywords and textA[v+1].isdigit():
                hourMinutes = textA[v+1].split(":")
                
                hours = hourMinutes[0]
                minutes = 0
                if len(hourMinutes) > 1:
                    minutes = hourMinutes[1]
                time = int(hours) * 100 + int(minutes)        
                Periodindex = v+2
                break
        if time is None:
            # if no time was found, check to see if there is a period in the text, sucas morning, afternoon, evening, night
            for v,a in enumerate(textA): 
                if a in periodKeywords:
                    Periodindex = v+1
                    break
                for x in textA[Periodindex:len(textA)]:
                    if x in nonPeriodDictionary:
                        time = nonPeriodDictionary.get(x)
                        break 
                
        else: 
            if Periodindex < len(textA):
                if textA[Periodindex].lower() == "pm":
                    time += 1200
            while time > 2400:
                time -= 2400
  
        return time
    def getEventDate(self, text):
        #find the keyword 'on' and then find the date that accomadates it:
        #get the date of the next day of the week
        keywords = ["on", "in", "at", "after", "before"]
        
        daysOfTheWeek = {"monday":0, "tuesday":1, "wednesday":2, "thursday":3, "friday":4, "saturday":5, "sunday":6}
        months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
        #get the date of today 
        today = datetime.date.today()
        outputDate = today
        test = ""
        cleanedText = text.replace("st ", "").replace("nd ", "").replace("rd ", "").replace("th ", "")
        textA = cleanedText.split(" ")
        for index, t in enumerate(textA):
            if t in keywords and index+1 < len(textA):
                if textA[index+1] in daysOfTheWeek:
                    outputDate = self.nextWeekday(today, daysOfTheWeek.get(textA[index+1]))
                    break
                
            elif t == "tomorrow":
                outputDate = datetime.date.today() + datetime.timedelta(days=1)
                break
            elif t == "week":
                outputDate = datetime.date.today() + datetime.timedelta(days=7)
                break
            elif t == "month":
                outputDate = datetime.date.today() + datetime.timedelta(days=30)
                break
            if t in ["the"] or t in months:
                if index+1 < len(textA):
                    if textA[index+1].isdigit():
                        test = "true"
                        outputDate = datetime.date(today.year,today.month,int(textA[index+1]))
        
        finaldate = f'{outputDate.month-1}-{outputDate.day}-{outputDate.year}'
        return finaldate
     
    def nextWeekday(self, date, weekday):
        days_ahead = weekday - date.weekday()
        if days_ahead <= 0: # Target day already happened this week
            days_ahead += 7
        return date + datetime.timedelta(days_ahead)
    def getEventDurationTime(self, text):
        #if there is the word 'at' inside the text, find the time that accomadates it: 
        keywords = ["for", "lasting"]
        textA = text.split(" ")
        duration = 90
        Periodindex = 0
        for v,a in enumerate(textA): 
            #turning time into military clock time 
            if a in keywords and textA[v+1].isdigit():    
                duration = int(textA[v+1])    
                Periodindex = v+2 
                break
        if Periodindex <= len(textA):
            if re.search("hour", textA[Periodindex]):
                duration = (duration) * 60
            elif re.search("minute", textA[Periodindex]):
                duration = int(duration)
            elif re.search("second", textA[Periodindex]):
                duration = int(duration) / 60
        
        return duration

    def getSubject(self, text):
        #if there is the word in SubjectKeywords is inside the text, then get the subject before or after it: 
        timeKeywords = ["for", "at", "in", "on", "after", "before"]
        dateKeywords = ["tomorrow", "today", "tonight", "when"]
        daysOftheWeek = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        startkeywords = ["do", "me", "make", "work", "to", "set", "create", "have", "a", "an"]

        textA = text.split(" ")
        startIndex = 0
        EndIndex = len(textA)
        
        for v,a in enumerate(textA): 
            #turning time into military clock time 
            if v < EndIndex:
                if a.isdigit():
                    EndIndex = v
                if a in timeKeywords:    
                    EndIndex = v
                if a in dateKeywords:
                    EndIndex = v
            if a in startkeywords:
                if v > startIndex:
                    startIndex = v                
            if a.lower() == "on":
                if v+1 < len(textA):
                    if textA[v+1] in daysOftheWeek and v < EndIndex:
                        EndIndex = v
        return " ".join(textA[startIndex:EndIndex])