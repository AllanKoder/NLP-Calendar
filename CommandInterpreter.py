from PyDictionary import PyDictionary
class CommandInterpreter:
    dictionary=PyDictionary()
    #create functions for eac   h command type
    def __init__(self):
        self.dictionary = PyDictionary()
    def interpret(self, command):
        if command[0] == 'define':
            return self.define(command[1])
        elif command[0] == 'synonym':
            return self.synonym(command[1])
        elif command[0] == 'antonym':
            return self.antonym(command[1])
        elif command[0] == 'example':
            return self.example(command[1])
        elif command[0] == 'translate':
            return self.translate(command[1])
        elif command[0] == 'play':
            return self.play(command[1])
        elif command[0] == 'help':
            return self.help()
        else:
            return 'Invalid command'
    def define(self, word):
        definition = self.dictionary.meaning(word)
        if definition == None:
            return 'No definition found'
        else:
            return definition
    def synonym(self, word):
        synonyms = self.dictionary.synonym(word)
        if synonyms == None:
            return 'No synonyms found'
        else:
            return synonyms
    def antonym(self, word):
        antonyms = self.dictionary.antonym(word)
        if antonyms == None:
            return 'No antonyms found'
        else:
            return antonyms
    def example(self, word):
        examples = self.dictionary.example(word)
        if examples == None:
            return 'No examples found'
        else:
            return examples
    def translate(self, word):
        translation = self.dictionary.translate(word)
        if translation == None:
            return 'No translation found'
        else:
            return translation
    def play(self, word):
        return 'Playing ' + word
    def help(self):
        return 'Available commands: define, synonym, antonym, example, translate, play, help'