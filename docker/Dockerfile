# ---- Base image ----
FROM python:3.10-slim

# ---- System setup ----
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# ---- Workdir ----
WORKDIR /app

# ---- Copy requirements ----
COPY requirements.txt .

# ---- Install dependencies ----
RUN pip install --no-cache-dir -r requirements.txt

# ---- Copy project ----
COPY app ./app
COPY data ./data

# ---- Expose FastAPI port ----
EXPOSE 8000

# ---- Run command ----
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
