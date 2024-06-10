## 0xGP Deployment infrastructure for Mac users 

Generate Lock 
```
pip-compile --generate-hashes --output-file=requirements-lock.txt requirements.in
```


Docker 

```
docker build -t 0xnrous-server:latest .
docker run -p 5000:5000 0xnrous-server:latest


# essential for last session to work
python your_flask_app.py
celery -A your_flask_app.celery worker --loglevel=info
redis-server
```

run local (Deployed application)
```
# essential to install the reqirments for python dependieces 
pip install requirements.txt
cd app/
python3 application.py
```



## 0xGP Deployment infrastructure for Windows users 

## run local (Deployed application)
```
## in program_files in C disk should have CMake and Python3 installed
## open vscode and command prompt and run the following commands

cmake --version

#### install it if it's not founded using command 

Invoke-WebRequest -Uri "https://github.com/Kitware/CMake/releases/download/v3.26.4/cmake-3.26.4-windows-x86_64.msi" -OutFile "cmake-3.26.4-windows-x86_64.msi"

# open 0xGP Deployment and install cmkae using GUI 
$env:Path += ";C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools\MSBuild\Current\Bin"
$env:Path += ";C:\Program Files\CMake\bin"
# open 0xGP Deployment  again if you not in this path 
mkdir build
cd build
cmake ..
cmake --build . --config Release
cmake --version
```



#### Step 2 : Setup virtual enviroment for python (requirements)
```
# in vscode open command prompt and run the following commands but in 0xGP Deployment folder 

python -m venv .venv

.venv\Scripts\activate

python -m pip install --upgrade pip

pip install numpy pandas matplotlib scikit-learn jupyter

pip install biopython

pip install Flask

pip install joblib

pip install lightgbm

pip install requests

pip install scipy

```



#### Step 3 : Run application in localhost 

```
# in vscode open command prompt and run make sure u are in 0xGP Deployment folder (prject folder using cd command) :dir 

cd app/

python3 application.py
```

#### now you can open http://localhost:5000 in browser 


