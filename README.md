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
3. **Essential Commands for Last Session**:
   ```bash
    python your_flask_app.py
    celery -A your_flask_app.celery worker --loglevel=info
    redis-server
   ```

#### For Windows Users

1. **Install CMake**:
   ```bash
   cmake --version

    # Install if not found
    Invoke-WebRequest -Uri "https://github.com/Kitware/CMake/releases/download/v3.26.4/cmake-3.26.4-windows-x86_64.msi" -OutFile "cmake-3.26.4-windows-x86_64.msi"

    # Open 0xGP Deployment and install CMake using GUI
   ```

2. **Setup Environment Paths**:
   ```bash
   $env:Path += ";C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools\MSBuild\Current\Bin"
   $env:Path += ";C:\Program Files\CMake\bin"
   ```

3. **Build Project**:

   ```bash
   mkdir build
   cd build 
   cmake ..
   cmake --build . --config Release
   cmake --version
   ```

4. **Setup Virtual Environment and Install Requirements**:

   ```bash
    python -m venv .venv
    .venv\Scripts\activate
    python -m pip install --upgrade pip

    pip install -r requirements.txt
   ```


#### 💻 Running the Application

#### Locally


1. **Install Requirements**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Run Application**:

   ```bash
   python application.py
   ```

3. **Access the Application**:
Open your browser and navigate to [http://localhost:5000](http://localhost:5000).


#### Using Docker

**Build and Run Docker Image**:

   ```bash
   docker build -t 0xnrous-server:latest .
   docker run -p 5000:5000 0xnrous-server:latest
   ```
## 📚 API Documentation

For detailed API documentation, please refer to the Postman collection: [0xGP API Documentation](https://documenter.getpostman.com/view/33483536/2sA3JT4Jzn).


## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
