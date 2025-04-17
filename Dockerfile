# === Base Image ===
FROM python:3.11-slim as base

# === System Setup ===
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# === Set workdir ===
WORKDIR /app

# === Install dependencies early for caching ===
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# === Copy app files ===
COPY . .

# === Expose Streamlit port ===
EXPOSE 8501

# === Entrypoint ===
CMD ["scripts/run-dev.sh"]