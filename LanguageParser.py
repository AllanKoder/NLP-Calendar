import pandas as pd
import numpy as np
import sys
from word2number import w2n
import re
from stopwords import commandstopwords, stopwords, subjectstopwords
from Dictionary import Dictionary
WordDictionary = Dictionary()

class LanguageParser:
    #algorithm order: remove all the weird punctuation, filter the numbers, time, classify the command, filter the stopwords, filter the words, filter the words in the dictionary
    def filter_words(self, text, set):
        #words after removing all the weird punctuation
        output = ""
        for w in text.split(" "):
            if w.lower() not in set:
                output += w + " "
        return output
        
    def classify(self, text):
        data = pd.read_csv("KeyWordsData.csv")
        data = data[data[['Duration','Reminder']].notna()]
        data[['Duration','Reminder']]=data[['Duration','Reminder']].astype(str)

        ReminderKeyWords = [x.lower().replace(" ", "") for x in data['Reminder'].tolist()]
        DurationKeyWords = [x.lower().replace(" ", "") for x in data['Duration'].tolist()]
        
        stop_words = set(stopwords.getwords())
        
        ReminderScore = 0
        DurationScore = 0
        
        filtered_sentence = []
        definitions = []
        BagOfWordsInput = []

        ReminderWordMap = {}
        DurationWordMap = {}
        
        command_stop_words = set(commandstopwords.getwords())
        filtered_sentence = self.filter_words(text, command_stop_words)
            
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
        return f"{returnoutput} D:{DurationScore} R:{ReminderScore}"
    def wordToNumber(self, text):
        try:
            return w2n.word_to_num(text)
        except:
            return None
    def wordToNumberSentence(self, text):
        textArray = text.split(" ")
        index = 0
        output = []
        #get all the words that are numbers and convert it to a number in digit form
        while (index < len(textArray)):
            if self.wordToNumber(textArray[index]):
                additionalString = textArray[index] + " " 
                for j in range(index+1, len(textArray)):
                    if (self.wordToNumber(textArray[j])):
                        additionalString += textArray[j] + " "
                        index+=1
                output.append(self.wordToNumber(additionalString))
            else:
                output.append(textArray[index])  
            index += 1
        return output
    def seperateTime(self,text):
        #clean out all numbers combined with time, such as pm and am 
        #check to see a character in the text is a number
        output = ""
        size = len(text)
        for c in range(size): 
            if text[c].isdigit():
                if c < size: 
                    if not text[c+1].isdigit():
                        #if the number is a digit while the proceeding char is not, that means it would like like a time abbreviation: example: 6pm
                        output += text[c] + " "
            else:
                output += text[c]
        return output
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
            if time > 2400:
                time -= 2400
  
        return time
                
    def getEventDurationTime(self, text):
        #if there is the word 'at' inside the text, find the time that accomadates it: 
        keywords = ["for"]
        textA = text.split(" ")
        duration = 120
        Periodindex = 0
        for v,a in enumerate(textA): 
            #turning time into military clock time 
            if a in keywords and textA[v+1].isdigit():    
                duration = textA[v+1]      
                Periodindex = v+2 
                break
        if Periodindex < len(textA):
            if re.search("hour", textA[Periodindex]):
                duration = int(duration) * 60
            elif re.search("minute", textA[Periodindex]):
                duration = int(duration)
            elif re.search("second", textA[Periodindex]):
                duration = int(duration) / 60
        
        return duration

    def getSubject(self, text):
        #if there is the word in SubjectKeywords is inside the text, then get the subject before or after it: 
        SubjectRegexes = ["at","for [^a-z]","tomorrow","next","today","tonight","when","in"]
        combinedRegexes = "(" + ")|(".join(SubjectRegexes) + ")"

        output = " "
        textA = text.split(" ")
        for v,a in enumerate(textA): 
            
            viewString = a + " "
            if v < len(textA)-1:
                viewString += textA[v+1]
            #if the word is in the SubjectKeywords regex looped through the text and get the subject
            if re.search(combinedRegexes, viewString):
                output = output.join(textA[:v+1])
                break
        #potential filtering in the future 
        # Subject_stop_words = set(subjectstopwords.getwords())
        # output = self.filter_words(output, Subject_stop_words)
        return output
    