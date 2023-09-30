import pyttsx3
import time

class Text_To_Speech():
    def __init__(self):
        self.engine = pyttsx3.init()

    def Run(self, text, gender='male', speed=160, save=False):
        if gender == 'male': self.engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\SPEECH\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0')
        else: self.engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')
        self.engine.setProperty('rate', speed)
        self.engine.say(text)
        if save: self.engine.save_to_file(text, f"{text[:int(len(text)/3)]}.mp3")
        self.engine.runAndWait()
    
    def stop_speech(self):
        self.engine.stop()
                
# text = "want you to create a python file script.py inside flutterproject folder in e drive"  
# Text_To_Speech().Run("Hi there! What can i do for you.", gender='male')