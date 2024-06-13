# 🛠️ 0xGP Deployment

This project provides infrastructure for deploying a machine learning model using Flask, Docker, and Celery, tailored for both Mac and Windows users.

## 📋 Table of Contents

- [🛠️ 0xGP Deployment](#️-0xgp-deployment)
  - [📋 Table of Contents](#-table-of-contents)
  - [🗂️ Project Structure](#️-project-structure)
  - [🚀 Getting Started](#-getting-started)
    - [🔧 Prerequisites](#-prerequisites)
    - [📦 Installation and Setup](#-installation-and-setup)
      - [For Mac Users](#for-mac-users)
      - [For Windows Users](#for-windows-users)
  - [💻 Running the Application](#-running-the-application)
    - [Locally](#locally)
    - [Using Docker](#using-docker)
  - [📚 API Documentation](#-api-documentation)
  - [📜 License](#-license)

## 🗂️ Project Structure

```
0xGP_Deployment/
├── models/
│   ├── random_forest_model.pkl
│   ├── tfidf_vectorizer.pkl
│   └── scaler.pkl
├── app/
│   └── application.py
├── templates/
│   ├── compare.html
│   ├── index.html
│   ├── missing.html
│   ├── predict.html
│   └── result.html
├── .dockerignore
├── .gitignore
├── Dockerfile
├── gunicorn_config.py
├── gunicorn.sh
├── Procfile
├── README.md
├── requirements-dev.in
└── requirements.txt
```


## 🚀 Getting Started

### 🔧 Prerequisites

- **Python 3**
- **Docker**
- **Redis**
- **Flask**
- **Celery**
- **Postman (for API testing)**

### 📦 Installation and Setup

#### For Mac Users

1. **Generate Lock File**:
   ```bash
   pip-compile --generate-hashes --output-file=requirements-lock.txt requirements.in
   ```

2. **Build Docker Image**:
   ```bash
   docker build -t 0xnrous-server:latest .
   docker run -p 5000:5000 0xnrous-server:latest
   ```


