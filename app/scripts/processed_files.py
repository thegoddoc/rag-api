import os, json, glob
from pathlib import Path
import pandas as pd

all_files = ''
def add_processed_files(all_files):
    names = [Path(file).name for file in all_files if Path(file).is_file()]
    print('NAMES:  \n'*2,names)
    return names
    

def get_processed_files():
    
    pass

if __name__ == '__main__':
    all_files = glob.glob(os.path.join('data','raw',"**", "*"), recursive=True)
    file = Path(all_files[-1])
    file_path = os.path.join('app', 'logs', 'processed_files.csv')
    print(f"Found {len(all_files)} files.\n {all_files[-1]}")
    print(f'FILE NAME:  {file}')
    names = add_processed_files(all_files)
    dt = pd.DataFrame(names)
    # with open('logs/processed_log.json', 'w') as f:
        # json.dump(names, f)
    with open(file_path, 'a') as f:
        dt.to_csv(f, header=False, index=False)
    with open(file_path, 'r') as f:
        lst = pd.read_csv(f)
    print(lst)
    print(lst['file_name'])
    if  lst['file_name'].str.contains('pdf').any():
        print(f'PRESENT ')
    else:
        print(f'NOT present')