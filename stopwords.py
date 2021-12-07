#use of polymorphism
stopword = {'only', 'off', 'weren','how', 'why', 'mightn', 'that', 'more', 'no', 's', "mightn't", 'll', 'when', 'didn', 'needn', 'theirs', 'which', 'is', 'wouldn', 'are', 'me', "she's", 'my', 'am', 'very', "you've", 'other', "wouldn't", 'ain', 'while', 'shan', 'doing', 'again', 'after', 've', 'to', 'will', "needn't", 'because', "couldn't", 'where', 'isn', "wasn't", 'yourself', 'her', 'such', 'he', "you'd", 'hasn', 'of', 'out', 'can', 'was', "you'll", 'each', 'won', 'these', 'shouldn', 'it', 'through', "isn't", 'wasn', "that'll", 'mustn', 'as', 'then', 'most', 'some', 'itself', "don't", "should've", 'i', 'below', 'have', 'with', 'your', 'here', 'o', "haven't", 'were', 'a', "doesn't", 'into', "you're", 'the', 'him', 'them', 'and', 'does', 'between', 'herself', 'all', 'she', 'do', 'its', 'from', 't', 'yours', "aren't", 'being', 'in', 'who', 'had', 'now', 'if', 'down', 'above', 'has', 'hadn', "won't", 'should', 'whom', 'be', 'what', 'ma', "shan't", 'having', 'or', 'both', 'yourselves', 'few', 'their', 'so', 'this', 'they', 'any', "it's", "hadn't", 'our', 'until', 'don', 'than', 'further', "didn't", 'nor', 'during', 'couldn', 'about', 'aren', 'himself', 'we', 'ourselves', 'd', 're', 'you', 'not', 'hers', 'there', 'just', 'an', 'themselves', 'against', 'under', 'same', 'been', "hasn't", "mustn't", 'doesn', 'over', 'his', 'ours', 'own', 'm', 'up', 'but', 'myself', "weren't", 'by', 'haven', "shouldn't", 'before', 'y', 'once', 'too', 'did', 'those'}
class stopwords:
    def getwords():
        #words used for filtering general text such as dictionaries
        seperatewords = {'at', 'for'}
        return stopword |seperatewords
class commandstopwords:
    def getwords():
        #words used for filtering the user input
        commandstopword = {'set', 'want', 'please'}
        return commandstopword | stopword