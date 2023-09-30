from _scripts.text_to_speech import Text_To_Speech
from nltk.corpus import stopwords
from actions import _Actions, _Action_Func
from threading import Thread
import spacy

nlp = spacy.load("en_core_web_sm") 

class _WINDOW_AUTOMATION():
    def __init__(self, voice=True):
        self.stop_words = set(stopwords.words('english'))
        self.nlp = nlp 
        self.voice = voice           
    
    def Run(self):
        if self.voice: self.Speech("Hi there! What can i do for you.")    
        user_command = input("VIRTUAL ASISTENT:") 
        user_command = [x.lower() for x in user_command.split(' ') if x.replace(' ', '') not in self.stop_words]
        user_command = ' '.join(user_command).lower()
        doc = self.nlp(user_command) 

        action = ""
        _opr_with = ""
        
        for token in doc:
            if token.text in _Actions.keys(): action = token.text
            
        for token in doc:
            if token.text in _Actions[action] and _opr_with == '': 
                _opr_with = token.text
        print(_opr_with)        
        _Action_Func[_opr_with](user_command, self.voice)
                
    def Speech(self, text, thread=True):
            def Translate():
                Text_To_Speech().Run(text)
            if thread:
                self.Speech_Thread = Thread(target=Translate)
                self.Speech_Thread.start()
            else: Text_To_Speech().Run(text)


while True:
    _WINDOW_AUTOMATION().Run()

    

    

