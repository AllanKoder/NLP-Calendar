class DateDataManager():
    def __init__(self):
        self.dateData = {}
        self.colorData = {}
        pass
    def addData(self, post):
        #add a post to the database using the date as the key and the post as the value, if the date does not exist, create it
        keyResult = self.dateData.get(post.get("date"))
        if keyResult is not None:
            keyResult.append(post)
            self.colorData[post.get("date")][post.get("color")] = True
        else:   
            #add a new date to the database
            self.dateData[post.get("date")] = [post]
            self.colorData[post.get("date")] = {post.get("color"):True}
    def getDate(self, date):
        return self.dateData.get(date)
    def deleteData(self, date, ID):
        #delete a post from the database using the unique color as the ID and the date as the key
        listOfEvents = self.dateData.get(date)
        if listOfEvents is not None:
            for i in listOfEvents:
                if i.get("color") == ID:
                    listOfEvents.remove(i)
                    break
            self.colorData[date][ID] = False
                
    def colorUsed(self, date, color):
        #check if a color is used in a date
        if self.colorData.get(date) == None:
            return False
        return self.colorData.get(date).get(color)
    def getWholeData(self):
        #return the entire database
        return str(self.dateData) + str(self.colorData)
    def findTotalEvents(self):
        # find the total amount of events in the database
        total = 0
        for i in self.dateData:
            total += len(self.dateData[i])
        return total
    def findAmountOfEachActivityPerDay(self):
        #find the amount of each activity in the database and return a dictionary with the activity as the key and the amount as the value
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