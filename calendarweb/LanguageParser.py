from io import StringIO
import pandas as pd
import numpy as np
import datetime
from word2number import w2n
import re
from calendarweb.stopwords import commandstopwords, stopwords, subjectstopwords
from calendarweb.Dictionary import Dictionary
WordDictionary = Dictionary()

class LanguageParser:
    #algorithm order: remove all the weird punctuation, filter the numbers, time, classify the command, filter the stopwords, filter the words, filter the words in the dictionary
    def __init__(self) -> None:
        self.keywordsData = pd.read_csv("calendarweb\KeyWordsData.csv")
        self.uncaptilizedWords = {"a":True,"an":True,"for":True,"of":True,"and":True,"on":True,"in":True,"at":True,"with":True,"the":True}
    def CapitalizeTitle(self, text):
        #split the text into words
        textArray = text.split(" ")
        textArray[0] = textArray[0].capitalize()
        #if the word is uncaptilized, then capitalize it
        #but if the word is in the uncaptilized list, then don't capitalize it
        for index, word in enumerate(textArray[1::]):
            if not self.uncaptilizedWords.get(word.lower()):
                textArray[index+1] = word.capitalize()        
        return (" ".join(textArray))
    def classifyActivity(self, text, catagories):
        #get the text in the csv file
        classData = self.keywordsData[self.keywordsData[catagories].notna()]
        classData[catagories]=classData[catagories].astype(str)

        classKeywords = [""]*len(catagories)
        for index, classTitle in enumerate(catagories):
            classKeywords[index] = [x.lower().replace(" ", "") for x in classData[classTitle].tolist() if x.lower() != "nan"]
        #create a data structure to manage the points for each catagory
        classScores = [0]*len(catagories)
        #create a map for the catagories
        ClassWordMap = [dict() for i in range(len(catagories))]
        
        for i in range(len(classKeywords)):
            for w in classKeywords[i]:
                ClassWordMap[i][w] = True

        #filter the words
        BagOfWordsInput = self.depthBagOfWords(text,1)

        #iterate through the text and check if the word is in the map
        for b in BagOfWordsInput:
            for i in range(len(ClassWordMap)):
                if ClassWordMap[i].get(b):
                    classScores[i] += 1
        #output the catagory with the highest score
        output = str(catagories[classScores.index(max(classScores))]).lower()
        return output

    def depthBagOfWords(self, text, depth):
        if depth == 0:
            return text
        else:
            return self.depthBagOfWords(" ".join(self.bagOfWords(text)), depth-1)
    def bagOfWords(self, text):
        #remove all the weird punctuation
        filtered_sentence = []
        BagOfWordsInput = []
        definitions = []
        command_stop_words = set(commandstopwords.getwords())
        stop_words = set(stopwords.getwords())
        #makes sures all the filter words are removed
        for w in text.split(" "):
            if w.lower() not in command_stop_words:
                filtered_sentence.append(w)
        #define all the words so there is more content
        for w in filtered_sentence:
            WordDefinition = WordDictionary.define(w)
            for key in WordDefinition:
                if isinstance(WordDefinition, dict):
                    for d in WordDefinition[key]:
                        definitions.append(d)
        #add all the words to the bag of words, such as definitions, filtered words and numbers
        totalwords = ""
        for s in definitions:
            totalwords += s + " "
        for s in filtered_sentence:
            totalwords += s + " "
        for w in totalwords.split(" "):
            if w.lower() not in stop_words:
                BagOfWordsInput.append(re.sub('[^a-zA-Z]+', '', w.lower()))
        return BagOfWordsInput
    def wordToNumber(self, text):
        #convert the word to a number
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
                # if the word is translatable to a number, then we want to replace it with the number
                additionalString = textArray[index] + " " 
                for j in range(index+1, len(textArray)):
                    if (self.wordToNumber(textArray[j])):
                        #if the word is still translatable to a number, then we want to add it to the number
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
                if text[v+1].isdigit() == False and text[v+1] != " " and text[v+1] != ":":
                    text = text[:v+1] + " " + text[v+1:]   
                    index += 1
        return text
    def getEventStartTime(self, text):
        #if there is the word 'at' inside the text, find the time that accomadates it: 
        textA = text.split(" ")
        time = 0
        found = False
        hourMinutes = None
        Periodindex = 0
        keywords = ["at", "after", "before", "on", "from"]
        periodKeywords = ["in", "on"]
        nonPeriodDictionary = {"morning": "900", "afternoon": "1200", "evening": "1800", "night": "2100","midnight": "0000", "noon": "1200", "midday": "1200","breakfast": "900", "lunch": "1200", "dinner": "1800",  "tonight": "1800"}
        for v,a in enumerate(textA): 
            #turning time into military clock time 
             if a in keywords and textA[v+1].replace(":","").isdigit():
                hourMinutes = textA[v+1].split(":")
                found = True
                Periodindex = v+2
                if hourMinutes[0] == "12":
                    Periodindex = 0
                break
        if found is False:
            # if no time was found, check to see if there is a period in the text, such as morning, afternoon, evening, night
            for v,a in enumerate(textA): 
                if a in periodKeywords:
                    Periodindex = v+1
                    break
                for x in textA[Periodindex:len(textA)]:
                    if x in nonPeriodDictionary:
                        #for all the words that can still be converted in a row, add them to the time. Such as (alarm for thirty five minutes)
                        time = nonPeriodDictionary.get(x)
                        break 
        else: 
            #use the index to find the pm and am, and add the time according to military time
            if Periodindex < len(textA):
                if textA[Periodindex].lower() == "pm":
                    time += 1200
                elif textA[Periodindex].lower() == "am":
                    while time >= 1200:
                        time -= 1200
            while time > 2400:
                time -= 2400
        if hourMinutes is not None:
            #attempt to use the hour and minutes to find the time
            #if there is an error with minutes, then only return hours
            try:
                return int(hourMinutes[0])*100 + (int(hourMinutes[1])/60)*100 + time
            except:
                return int(hourMinutes[0])*100 + time
        else: 
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
        cleanedText = text.replace("st ", "").replace("nd ", "").replace("rd ", "").replace("th ", "")
        textA = cleanedText.split(" ")
        for index, t in enumerate(textA):
            if t in keywords and index+1 < len(textA):
                if textA[index+1] in daysOfTheWeek:
                    #use the day of the week to find the date
                    outputDate = self.nextWeekday(today, daysOfTheWeek.get(textA[index+1]))
                    break
            #if the word is a amount of time, add the according time to the date
            if t == "tomorrow":
                outputDate = datetime.date.today() + datetime.timedelta(days=1)
                break
            elif t == "week":
                outputDate = datetime.date.today() + datetime.timedelta(days=7)
                break
            elif t == "month":
                outputDate = datetime.date.today() + datetime.timedelta(days=30)
                break
            if t in ["the"] or t in months:
                #if the word is a date, such as (on the) 27th, then we want to use the date
                if index+1 < len(textA):
                    if textA[index+1].isdigit():
                        outputDate = datetime.date(today.year,today.month,int(textA[index+1]))
            if t in months:
                #if it is a month, then find the date of the month
                outputDate = datetime.date(today.year,months.index(t)+1,outputDate.day)
                if months.index(t)+1 < today.month:
                        outputDate = datetime.date(today.year+1,months.index(t)+1,outputDate.day)
        finaldate = f'{outputDate.month-1}-{outputDate.day}-{outputDate.year}'
        return finaldate
     
    def nextWeekday(self, date, weekday):
        #find how many days until the next weekday and if the next weekday is not in the future, make it the next week
        days_ahead = weekday - date.weekday()
        if days_ahead <= 0: # Target day already happened this week
            days_ahead += 7
        return date + datetime.timedelta(days_ahead)
    def getEventDurationTime(self, text):
        #if there is the word 'at' inside the text, find the time that accomadates it: 
        keywords = ["for", "lasting","of"]
        textA = text.split(" ")
        duration = None
        Periodindex = len(textA)+1
        for v,a in enumerate(textA):    
            #turning time into military clock time 
            if a in keywords and textA[v+1].isdigit():    
                duration = int(textA[v+1])    
                Periodindex = v+2
                break
            if a == "from":
                try:
                    #get find the integers b
                    startMin = 0
                    EndMin = 0
                    startMidday = "pm"
                    endMidday = "pm"
                    startTime = textA[v+1].split(":")
                    startHours = int(startTime[0])
                    #if the start time is in the afternoon, then set the startMidday to pm
                    if startTime[0] == "12":
                        startHours = 0
                    #this is the predicted endindex, however with formatting, we have to find the correct time 
                    endIndex = v+3
                    
                    if textA[endIndex] == "to":
                        endIndex += 1        
                    if textA[endIndex] in ["pm", "am"]:
                        endMidday = textA[endIndex]
                    if textA[v+1] in ["pm", "am"]:
                        startMidday = textA[v+1]    
                      
                    endTime = textA[endIndex].split(":")
                      
                    #if the len is 2, then it includes minutes 
                    if len(endTime) > 1:
                        EndMin = int(endTime[1])
                    if len(startTime) > 1:
                        startMin = int(startTime[1])
                   
                    #return the time in military time
                    duration = self.getDurationfromTime((startHours*60+startMin), startMidday, int(endTime[0])*60 + (EndMin), endMidday)
                except Exception as e:
                    return str(e)
                    
        if Periodindex <= len(textA):
            #multiply the time by the unit, such as hours, minutes and seconds, and return the time so it is in minutes 
            if re.search("hour", textA[Periodindex]):
                duration = (duration) * 60
            elif re.search("minute", textA[Periodindex]):
                duration = int(duration)
            elif re.search("second", textA[Periodindex]):
                duration = int(duration) / 60
        
        return duration
    def getDurationfromTime(self, startTime, startMidday, endTime, endMidday):
        #starttime is in minutes time and combined miltary time. 
        totalTime = 0
        if startMidday == endMidday:
            if startTime > endTime:
                startMidday = "am"
            else:
                totalTime = endTime - startTime
        #If there is a difference in midday, then we add the difference from 12pm and add the other time 
        if startMidday == "pm" and endMidday == "am":
            totalTime += abs(600 - endTime) + startTime
        elif startMidday == "am" and endMidday == "pm":
            totalTime += abs(600 - startTime) + endTime
        return abs(totalTime)
    
    def getSubject(self, text):
        #if there is the word in SubjectKeywords is inside the text, then get the subject before or after it: 
        timeEndKeywords = ["for", "at", "in", "on", "after", "from", "before"]
        dateKeywords = ["tomorrow", "today", "tonight", "week", "month"]
        daysOftheWeek = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        startkeywords = ["do", "me", "make", "work", "set", "have", "a", "an"]

        textA = text.lower().split(" ")
        startIndex = 0
        EndIndex = len(textA)
        
        for v,a in enumerate(textA): 
            #if the sentence starts with a keyword, then we want to start at the next word
            #if the word is a time, then we want to end at the time
            #whenever there is a keyword with a proceeding number or time, we want to end at the keyword
            #if there is a word in a array, we want to set the end or start index depending on the word
            if v < EndIndex:
                if a.isdigit():
                    EndIndex = v
                if a in timeEndKeywords:
                    if textA[v+1].isdigit() or ":" in textA[v+1]:    
                        EndIndex = v
                if a in dateKeywords and v > startIndex:
                    EndIndex = v
            if a in startkeywords:
                if v > startIndex:
                    startIndex = v                
            if a.lower() == "on":
                if v+1 < len(textA):
                    if textA[v+1] in daysOftheWeek and v > EndIndex:
                        EndIndex = v
            o = " ".join(textA[startIndex:EndIndex])
            for s in daysOftheWeek:
                o = o.replace(s, "")
        return o