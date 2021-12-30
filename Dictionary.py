from PyDictionary import PyDictionary
class Dictionary:
    dictionary=PyDictionary()
    #create functions for each command type
    def __init__(self):
        self.dictionary = PyDictionary()
    def define(self, word):
        try: 
            definition = self.dictionary.meaning(word)
            if definition == None:
                return ""
            else:
                return definition
        except:
            return ""
    def synonym(self, word):
        try: 
            synonyms = self.dictionary.synonym(word)
            if synonyms == None:
                return ""
            else:
                return synonyms
        except:
            return ""
    def antonym(self, word):
        try: 
            antonyms = self.dictionary.antonym(word)
            if antonyms == None:
                return ""
            else:
                return antonyms
        except:
            return ""
    def example(self, word):
        try: 
            examples = self.dictionary.example(word)
            if examples == None:
                return ""
            else:
                return examples
        except:
            return ""
    def translate(self, word):
        try:
            translation = self.dictionary.translate(word)
            if translation == None:
                return ""
            else:
                return translation
        except:
            return ""