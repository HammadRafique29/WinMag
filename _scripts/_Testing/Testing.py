import Test_Dumpy_data
import re

class File_Management_Testings():
    def __init__(self):
        pass
    
    def _CREATE_FILE_TESTING(self):
        test_commands = Test_Dumpy_data._Create_File_Commands
        for index, user_command in enumerate(test_commands):
            file_type = r"{}[\s]*([\w]+)[\s]*file"
            file_name_pattern =  r"\s*(?: (?:file[\s]*|[\s]*named)|(?:file\snamed))[\s]+(?:([\w\s]+\.[\w]+)|(?:([\w\s]*)\s+inside)|([\w\s]*)inside|([\w]+[\s]*))"
            folder_name_pattern = r"\s(?:(?:inside)|(?:file\sinside)|(?:file\s(?!inside)))\s([\w\s]+)\sfolder"
            drive_name_pattern = "\s(.)\sdrive"

            File_Type = re.findall(file_type.format("create"), user_command )
            File_Name = re.findall(file_name_pattern.format("create"), user_command)
            Folder = re.findall(folder_name_pattern.format("create"), user_command )
            Drive = re.findall(drive_name_pattern.format("create"), user_command )
            
            result = []
            if File_Type: 
                File_Type = ''.join(File_Type[0]) 
                result.append(File_Type)
            if File_Name: 
                File_Name = ''.join(File_Name[0])
                result.append(File_Name) 
            if Folder: 
                Folder = ''.join(Folder[0])
                result.append(Folder)
            if Drive: 
                Drive = ''.join(Drive[0].lower())
                result.append(Drive)
            if test_commands[user_command][0] == len(result):
                for index, data in enumerate(result):
                    if test_commands[user_command][1][index] != data:
                        print("Failed")
                        break
            else:
                print("Failed")
                continue    
            print(f"Success -- {result}")
            
            
File_Management_Testings()._CREATE_FILE_TESTING()