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


## ⚡ Step 3: Build and Run WIth DOcker
### 🐳 Step 1 — Install Docker Engine (Recommended) EXAMPLE (LINUX MINT)
Run these commands one by one in your terminal:
```bash

# 1. Remove the broken Docker repo
sudo rm /etc/apt/sources.list.d/docker.list 2>/dev/null

# 2. Add the correct Docker GPG key
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# 3. Add Docker repo manually (force to Ubuntu noble)
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
  https://download.docker.com/linux/ubuntu noble stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```
```bash
# 4. Update package list
sudo apt update

# 5. Install Docker CE and Compose
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y

```



### From project root (rag-fastapi/):
```bash
sudo docker compose build
docker compose up
```

Now open:
👉 http://127.0.0.1:8000/docs
Your FastAPI RAG API runs inside Docker, connected to ChromaDB.


## 🧠 Step 4: Stop / Rebuild
```bash
docker compose down        # stop containers
docker compose up -d       # restart in background
docker compose build --no-cache   # rebuild everything
```

## 🐳 If you Want to REMOVE Docker container/image 
Check what’s running:
```bash
docker ps -a
```
Then remove the container:
```bash
docker rm -f rag-api-api
```
And if you want to remove the image too:
```bash
docker rmi rag-api-api
```

To remove all containers and images:
```bash
docker rm -f $(docker ps -aq)
docker rmi -f $(docker images -q)
```


