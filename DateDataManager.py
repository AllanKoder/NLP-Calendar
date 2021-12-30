class DateDataManager():
    def __init__(self):
        self.data = {}
        pass
    def addData(self, post):
        keyResult = self.data.get(post.get("date"))
        if keyResult is not None:
            keyResult.append(post)
        else:
            self.data[post.get("date")] = [post]
    def getDate(self, date):
        return self.data.get(date)
    def getWholeData(self):
        return self.data