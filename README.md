# rag-api
RAG fast api local 


## make virtual environment and install
```bash
python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt
```


## Install llama.cpp for Local llm system.
### Install Homebrew for Linux
To install Homebrew on Linux Mint, follow these steps:
Open a terminal: You can usually find the terminal in your applications menu or by pressing Ctrl + Alt + T.
Ensure prerequisites are installed: Homebrew requires build-essential and curl. Install them if they are not already present:
Code
```bash

    sudo apt update
    sudo apt install build-essential curl
Run the Homebrew installation script: Execute the following command in your terminal. This command downloads and runs the official Homebrew installation script.
```
Code
```bash

    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install
```

### HAndle llama-cpp-python installement
✅ Solution options (from simplest to cleanest)
Option 1 — Use system compiler (recommended)
Run this once before building:
```bash
export CC=/usr/bin/gcc
export CXX=/usr/bin/g++
```

Then reinstall:
```bash
pip install --force-reinstall --no-cache-dir llama-cpp-python
That tells CMake to use the system gcc/g++, which can find libgomp automatically.
```

python -c "import llama_cpp; print('✅ llama-cpp-python works!')"

## RUN UVICORN server:
from within the directory of app/ wich contain main.py
run:
```bash
uvicorn main:app --reload
```

### For DOcs 
```bash
localhost:port/docs
```

## API 
### RAG Query 
post request with data dectionary containing query, k: no of chunks to be retrived , mood: string from 3 values (retrive, rerank, report)
Example usage :

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/query?mode=retrive' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "query": "panadol",
  "k": 4
}'
```

#### Request URL
```bash
import requests

url = "http://127.0.0.1:8000/query?mode=retrive"
headers = {
    "accept": "application/json",
    "Content-Type": "application/json"}
    
data = {"query": "panadol", "k": 4}

response = requests.post(url, headers=headers, json=data)

print(response.status_code)
print(response.json())


```


