# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements files into the container at /app
COPY requirements*.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip \
    && pip install -r requirements-lock.txt

# Copy the application code into the container at /app
COPY app /app/app
COPY templates /app/templates

# Define environment variable
ENV NAME !needlman-api-AWS

# Make port 8000 available to the world outside this container
EXPOSE 8000

RUN chmod +x gunicorn.sh

# Run gunicorn server with the specified configuration file
CMD ["sh", "gunicorn.sh"]


# !needlman-api-AWS/
# │
# ├── app
# |    ├── application.py
# |
# ├── templates
# |    ├── index.html
#      ├── missing.html
#      ├── result.html
# ├── Dockerfile
# ├── .dockerignore
# ├── requirements.in
# ├── requirements-lock.txt
# ├── requirements-dev.txt
# ├── gunicorn_config.py
# └── gunicorn.sh
