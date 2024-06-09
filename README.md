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



