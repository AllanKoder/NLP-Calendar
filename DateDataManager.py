class DateDataManager():
    def __init__(self):
        self.dateData = {}
        self.colorData = {}
        pass
    def addData(self, post):
        keyResult = self.dateData.get(post.get("date"))
        if keyResult is not None:
            keyResult.append(post)
            self.colorData[post.get("date")][post.get("color")] = True
        else:   
            self.dateData[post.get("date")] = [post]
            self.colorData[post.get("date")] = {post.get("color"):True}
    def getDate(self, date):
        return self.dateData.get(date)
    def deleteData(self, date, ID):
        listOfEvents = self.dateData.get(date)
        if listOfEvents is not None:
            for i in listOfEvents:
                if i.get("color") == ID:
                    listOfEvents.remove(i)
                    break
            self.colorData[date][ID] = False
                
    def colorUsed(self, date, color):
        if self.colorData.get(date) == None:
            return False
        return self.colorData.get(date).get(color)
    def getWholeData(self):
        return str(self.dateData) + str(self.colorData)
    

    