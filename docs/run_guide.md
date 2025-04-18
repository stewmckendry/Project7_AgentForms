# 🏃‍♂️ Run Guide: Concussion Agent App

This guide shows you how to run the Concussion Agent app both locally and on Azure.

---

## 🖥️ Run Locally (Development)

### 1. ✅ Set up environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. 🛠️ Set environment variables
Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your-key-here
```

### 3. 🚀 Start the app
```bash
# Run the FastAPI backend
uvicorn src.server.main:app --reload --port 8001

# In a new terminal, run the Streamlit client
streamlit run src/client/app.py
```

App will be live at: `http://localhost:8501`

---

## ☁️ Run on Azure (Docker + App Service)

> Uses Azure App Service with custom container from ACR.

### 1. 🔧 Build & Push Docker Image
```bash
./scripts/dev-push.sh
```

### 2. 🚀 Deploy to Azure
```bash
./scripts/deploy.sh
```

### 3. 🔍 Check Status / Logs
```bash
./scripts/status.sh
```

---

## 📦 Other Utilities
```bash
./scripts/start.sh         # Local full app runner
./scripts/deactivate.sh    # Kill running dev processes
./scripts/reactivate.sh    # Reconnect and test after deploy
```

---

## 🧠 Notes
- Streamlit runs on port 8501
- FastAPI runs on port 8001
- Both apps share the same container on Azure
- Make sure your ACR and App Service settings are correctly configured

For any issues, inspect logs in Azure portal or via the `status.sh` script.
