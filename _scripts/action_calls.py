from bin.data import programming_extensions
from _scripts.text_to_speech import Text_To_Speech
from threading import Thread
import subprocess
from pathlib import Path
import pyttsx3
import spacy
import random
import time
import re
import os

nlp = spacy.load("en_core_web_sm")

class _CREATE_ACTION_FUNCTIONS():
    def __init__(self):
        self.default_dir = "E:/"
          
    def Speech(self, text, thread=True):
            def Translate():
                while True:
                    try:
                        Text_To_Speech().stop_speech()
                        Text_To_Speech().Run(text)
                        break
                    except: pass
            if thread:
                self.Speech_Thread = Thread(target=Translate)
                self.Speech_Thread.start()
            else: 
                while True:
                    try:
                        Text_To_Speech().stop_speech()
                        Text_To_Speech().Run(text) 
                        break
                    except: pass
                
    def _CREATE_FILE(self, *args):
        
        file_type = r"{}[\s]*([\w]+)[\s]*file"
        # file_name_pattern =  r"\s*(?: (?:file[\s]*|[\s]*named)|(?:file\snamed))[\s]+(?:([\w\s]+\.[\w]+)|(?:([\w\s]*)\s+inside)|([\w\s]*)inside)"
        file_name_pattern =  r"\s*(?: (?:file[\s]*|[\s]*named)|(?:file\snamed))[\s]+(?:([\w\s]+\.[\w]+)|(?:([\w\s]*)\s+inside)|([\w\s]*)inside|([\w]+[\s]*))"
        folder_name_pattern = r"\s(?:(?:inside)|(?:file\sinside)|(?:file\s(?!inside)))\s([\w\s]+)\sfolder"
        drive_name_pattern = "\s(.)\sdrive"
        
        
        user_command = self.clean_command(args[0])
        
        File_Type = re.findall(file_type.format("create"), user_command )
        File_Name = re.findall(file_name_pattern.format("create"), user_command)
        Folder = re.findall(folder_name_pattern.format("create"), user_command )
        Drive = re.findall(drive_name_pattern.format("create"), user_command )
        
        print(File_Name)
        
        if File_Type: File_Type = ''.join(File_Type[0]) 
        else: File_Type = ''
        if File_Name: File_Name = ''.join(File_Name[0])
        else: File_Name = ''
        if Folder: Folder = ''.join(Folder[0])
        else: Folder = ''
        if Drive: Drive = ''.join(Drive[0].capitalize()+":\\")
        else: Drive = ''
        
        if File_Type != '' and '.' not in File_Name:
            if File_Type in programming_extensions.keys(): 
                File_Name = File_Name + "." + programming_extensions[File_Type]
        self.validate_file_management_command([File_Name, Folder, Drive], _for="file")

    def _CREATE_FOLDER(self, *args):
        message = self.clean_command(args[0])
        
        folder_name_pattern = r"[\w\d\s]*{0}\sfolder\s((?:(?!\sinside\b)[\w\s_])+)".format("create")
        parent_folder_pattern = r"\s(?:(?:inside))\s([\w\s]+)\sfolder"
        drive_name_pattern = "\s([a-z])\sdrive[\w\s\d.]*"
        
        Folder = re.findall(folder_name_pattern, message)
        Parent_Folder = re.findall(parent_folder_pattern, message)
        Drive = re.findall(drive_name_pattern, message)
        
        if Folder: Folder = Folder[0] 
        else: Folder = ''
        if Parent_Folder: Parent_Folder = Parent_Folder[0]
        else: Parent_Folder = ''
        if Drive: Drive = Drive[0].capitalize()+":\\"
        else: Drive = ''
        self.validate_file_management_command([Folder, Parent_Folder, Drive], _for="folder")
    
    def clean_command(self, message):
        message = message.lower()
        message = ' '.join(message.split())
        return message

    def RESPONSE_BACK(self, text, path, voice):
        print(text)
        # self.Speech(text.replace(str(path), ''))
        self.Speech(voice)

    def validate_file_management_command(self, command, _for): 
        Name, Folder, Drive = command[0], command[1], command[2]
        path, current_dir = '', os.getcwd()
        action = ''
        if "fol" in _for: action = "mkdir"
        if "fil" in _for: action = "echo. > "
        
        _DIR_CHECK = self._FIND_FOLDER_DIRECTORY(Drive, Folder)
        
        if _DIR_CHECK[1]: 
            if len(_DIR_CHECK[1]) == 1: Folder = _DIR_CHECK[1][0]
                
            if len(_DIR_CHECK[1]) > 1:
                mutiple_values = ', '.join(_DIR_CHECK[1])
                self.RESPONSE_BACK(f"There is  multiple directories with same name. Which one to select [{mutiple_values}]", mutiple_values, "Found Many Directories")
                select = int(input("Enter index: "))
                Folder = _DIR_CHECK[1][select-1].replace(Drive, '')
                
        elif _DIR_CHECK[0][1] and not _DIR_CHECK[1]:
            value = _DIR_CHECK[0][1]
            self.RESPONSE_BACK(f"I found the similar directory, {_DIR_CHECK[0][1].replace(Drive, '')}, instead of {Folder}.", '', "Found Similar Directory")
            select = input("Continue [Y/N]: ")
            if select.lower() == 'y': Folder = _DIR_CHECK[0][1]
            else: return 0
            
        elif not _DIR_CHECK[0] and not _DIR_CHECK[1]:
            self.RESPONSE_BACK(f"Directory {Folder} not found", '', 'Directory Not Found')
            return 0
            
        if Name == '': self.RESPONSE_BACK(f"You forgot to provide {_for} name.", path, f'Provide {_for} Name')

        if Name != '' and Folder == '' and Drive == '':
            path = current_dir +"/"+Name
            if not os.path.exists(path):
                try: 
                    subprocess.check_output(f"{action} \"{path}\"", shell=True, stderr=subprocess.STDOUT, encoding='utf-8')
                    self.RESPONSE_BACK(f"Successfully created {Name} {_for} inside current directory.", path, f'{_for} is Created')  
                except Exception as e: 
                    try: result = str(e.output)
                    except: result = str(e)
                    finally: self.RESPONSE_BACK(result, path)
            else: RESPONSE_BACK(f"Given {_for} already exists.", path, f'{_for} Already Exists')
            
            
        if Name != '' and Folder != '' and Drive == '':
            path = current_dir+"/"+Folder+"/"+Name
            if not os.path.exists(path):
                try: 
                    subprocess.check_output(f"{action} \"{path}\"", shell=True, stderr=subprocess.STDOUT, encoding='utf-8')
                    self.RESPONSE_BACK(f"Successfully created {Name} inside {Folder} in current directory.", path, f'{_for} is Created')
                except Exception as e: 
                    try: result = str(e.output)
                    except: result = str(e)
                    finally: self.RESPONSE_BACK(result, path, f'{result.replace(path)}')
            else: self.RESPONSE_BACK(f"Given {_for} already exists.", path, f'{_for} Already Exists')
            

        if Name != '' and Folder != '' and Drive != '':
            path = os.path.join(Drive, Folder, Name)
            if not os.path.exists(path):
                try: 
                    result = subprocess.check_output(f'{action} \"{path}\"', shell=True, stderr=subprocess.STDOUT, encoding='utf-8')
                    self.RESPONSE_BACK(f"Successfully created {Name} {_for} inside {Folder}", path, f'{_for} is Created')   
                except Exception as e: 
                    try: result = str(e.output)
                    except: result = str(e)
                    finally: self.RESPONSE_BACK(result, path, f'{result.replace(path)}')
            else: self.RESPONSE_BACK(f"Given {_for} already exists.", path, f'{_for} Already Exists')
        
    def _FIND_FOLDER_DIRECTORY(self, top_level_dir, folder_name):
            Expected_Folder, matched_folder = [folder_name, folder_name.replace(' ', '_'), folder_name.replace(' ', '')], []
            target, similar_result = nlp(folder_name), [0.0, None]
            for root, dirs, files in os.walk(top_level_dir):
                for folders in dirs:
                    Result = re.findall( r"(?:[\w\s\d_]*{0}[\w\s\d_]*)|(?:[\w\s\d_]*{1}[\w\s\d_]*)|(?:[\w\s\d_]*{2}[\w\s\d_]*)".format(Expected_Folder[0], Expected_Folder[1], Expected_Folder[2]), folders.lower())
                    if Result:
                        ratio = nlp(folder_name).similarity(nlp(folders))
                        if ratio > similar_result[0]: similar_result = [ratio, os.path.join(root.capitalize(), Result[0])]
                        if Result[0].lower() in Expected_Folder:
                            matched_folder.append(os.path.join(root.capitalize(), Result[0]))
            return similar_result, matched_folder
    
    def _GENERATE_FILE_NAME(self, directory, filename):
        if self._FIND_DUPLICATE_FILE(directory, filename):
            filename = filename.split('.')
            filename = filename[0]+str(random.randrange(1, 100))+"."+filename[1]
            return self._GENERATE_FILE_NAME(directory, filename)
        else: 
            return filename
        
    def _FIND_DUPLICATE_FILE(self, directory, filename):
        file_path = os.path.join(directory, filename)
        return os.path.isfile(file_path) 
 