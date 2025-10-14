import os, glob
import shutil
from pathlib import Path
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename

class FileUpload():
    def __init__(self):
        self.filename=''
        self.folder = '/home/mohamed/Downloads/'
    
    def select_file(self):
        all_files = os.listdir(self.folder)
        for i, file in enumerate(all_files):
            print(f'NO: {i}  Filr: {file}')
        x = int(input('PLEASE SELECT FIleNO TO UPLOAD'))
        self.filename = all_files[x]
        print(f'SLECTED FILE IS :  {self.filename}')

    def select_file_sc(self):
        win = Tk()
        # win.attributes('-topmost')
        win.withdraw()
        # win.focus_force()
        # top = Toplevel()
        if self.folder:
            filename = filedialog.askdirectory()
        else:
            filename = askopenfilename(parent=win)
        print(filename)
        self.filename = filename
        return filename
    #  copy file to raw directory.
    def add_file(self, categ ='product'):
        all_categ = glob.glob(os.path.join('data', 'raw','**','*'), recursive=True)
        all_categ = [dir for dir in all_categ if not Path(dir).is_file()]
        source_file = os.path.join(self.folder,self.filename)
        for i,file in enumerate(all_categ):
             print(f'NO: {i}, FILE: {file}')
        inp = int(input('INPUT  CATEG NO'))
        categ = all_categ[inp]
        print(f'SELECTED CATEGORY IS: {categ}')
        # Define the destination directory path
        destination_directory = os.path.join('data', 'raw', categ)
        print(f'DESTINATION : {destination_directory}')
        # Ensure the destination directory exists (optional, but good practice)
        # os.makedirs(destination_directory, exist_ok=True)
        try:
            # Copy the file to the destination directory
            # shutil.copy(source_file, destination_directory)
            print(f"File '{source_file}' successfully copied to '{destination_directory}'")
        except FileNotFoundError:
            print(f"Error: Source file '{source_file}' not found.")
        except PermissionError:
                print(f"Error: Permission denied when trying to copy to '{destination_directory}'.")
        except shutil.SameFileError:
                print("Error: Source and destination represent the same file.")
        except Exception as e:
                print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
     x = FileUpload()
     x.select_file()
     x.add_file()
        
    

    


