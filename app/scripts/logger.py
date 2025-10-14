import json
from configs.config import rag_config
'ERROR_RAG_LOG, BUILD_INDEX'
from datetime import datetime
# from zoneinfo import ZoneInfo

# Create a timezone object for Cairo
# cairo_tz = ZoneInfo("Africa/Cairo")

log_file = rag_config['ERROR_RAG_LOG']

def insert_err(e):
    with open(log_file, 'r') as f:
        json.dump(e, f)

class Logger():
    def __init__(self, name: str, logs: list):
        if len(logs) ==0:
            pass
        self.name = name
        self.logs = logs
    
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
            pass

    def insert_(self, message, fp):
        with open(fp, 'r') as f:
            json.dump(message, f)





