import json
from app.configs.config import rag_config
'ERROR_RAG_LOG, BUILD_INDEX'
from datetime import datetime
import pandas as pd
from typing import Literal
# from zoneinfo import ZoneInfo

# Create a timezone object for Cairo
# cairo_tz = ZoneInfo("Africa/Cairo")

log_file = rag_config['ERROR_RAG_LOG']
embedded = rag_config['EMBEDDED_CHUNKS']
processed = rag_config['PROCESSED_FILES']

def insert_err(e):
    with open(log_file, 'r') as f:
        json.dump(e, f)

class Logger():
    def __init__(self):
        self.name = 'name'
        self.logs = ['logs']
    
    def log(self):
        routs = [
            {'build_index': rag_config['BUILD_INDEX']}
        ]
        try:
            fp = [item[f'name'] for item in routs][0]
            self.insert_(self.logs, fp)
        except Exception as e:
            e = {'function':self.name, 'time': datetime.now(), 'error':''}
            insert_err(e)

    def insert_(self, message, fp):
        with open(fp, 'r') as f:
            json.dump(message, f)
    
    def log_processed(self, lst:list, type:Literal['embed', 'process']):
        if type== 'embed':
            fp = embedded
        elif type == 'process':
            fp = processed
        dt = pd.DataFrame(lst)
        with open(fp, 'a') as f:
            dt.to_csv(f, index=False, header=False)
    
    






