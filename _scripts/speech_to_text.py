import speech_recognition as sr

class To_Text():
    def __init__(self):
        self.recognizer = sr.Recognizer()
        
    def Run(self, file):
        # Open the audio file and recognize speech
        with sr.AudioFile(file) as source:
            # Adjust for ambient noise if necessary
            self.recognizer.adjust_for_ambient_noise(source)
            # Listen for speech and convert it to text
            try:
                audio_data = self.recognizer.record(source)  # Record the audio data
                audio_text = self.recognizer.recognize_google(audio_data)
                print("Recognized text:", audio_text)
            except sr.UnknownValueError:
                print("Google Web Speech API could not understand the audio")
            except sr.RequestError as e:
                print("Could not request results from Google Web Speech API; {0}".format(e))


class OpenAI_Speech_To_Text():
    import openai
    
    def __init__(self):
        self.api = self.get_api()
        self.example = {"text": "I want you to create a Python file script.py inside Flutter project folder in E drive."}
    
    def get_api(self):
        with open("./bin/include/api.txt") as file:
            data = file.readline()
            return data
    
    def Run(self, file):
        try:
            print(self.example["text"])
            # audio_file= open(file, "rb")
            # transcript = openai.Audio.transcribe("whisper-1", audio_file)
            # return transcript
        except Exception as e: print(e)
        
            

OpenAI_Speech_To_Text().Run("test")
        
# import openai

# audio_file= open("I want you to create a pytho.mp3", "rb")
# transcript = openai.Audio.transcribe("whisper-1", audio_file)
# print(transcript)