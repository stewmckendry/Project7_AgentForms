# 🚀 Concussion Agent Deployment Guide

This document outlines how to build, push, and deploy the Concussion Agent app to Azure using Docker and shell scripts.

---

## 🐳 1. Build and Push Docker Image

```bash
bash dev-push.sh
```

- Builds the Docker image for the app
- Tags it as `concussion-agent`
- Pushes it to your Azure Container Registry (`agentformsacr`)

---

## ☁️ 2. Create Azure Resources

```bash
bash setup.sh
```

- Creates:
  - Resource Group: `baseball-tutor-rg`
  - App Service Plan: `agentforms-plan`
  - Web App: `concussion-agent-app`
- Configures it to pull from your ACR

---

## 🚀 3. Deploy Updated Image to Azure

```bash
bash deploy.sh
```

- Updates the web app container to the latest pushed image
- Restarts the web app and checks status

---

## 🔁 4. Reactivate or Restart the App

```bash
bash reactivate.sh
```

- If the app is stopped or deleted, re-creates and re-deploys

---

## 🧹 5. Optional: Stop or Delete the App

```bash
bash deactivate.sh
```

- Stop or delete the `concussion-agent-app` on Azure
- Useful for clean-up or cost control

---

## 📊 6. Check App Status

```bash
bash status.sh
```

- Verifies if the web app is running and healthy
- Outputs current state (e.g., Running, Stopped)

---

## 📦 Deployment Notes

- The app exposes **Streamlit on port 8501** and **FastAPI on port 8001**
- You can debug live logs in Azure Portal via **Kudu console**

---

Made with 🧠 + 💬 by ChatGPT + Stewart McKendry