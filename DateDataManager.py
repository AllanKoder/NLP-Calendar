class DateDataManager():
    def __init__(self):
        self.data = {}
        pass
    def addData(self, post):
        self.data[post[0].get("date")] = post
    def getDate(self, date):
        return self.data.get(date)
    def getWholeData(self):
        return self.data