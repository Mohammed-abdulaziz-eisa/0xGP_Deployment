# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements files into the container at /app
COPY requirements*.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip \
    && pip install -r requirements-lock.txt

# Copy the rest of the working directory contents into the container at /app
COPY . /app

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME !needlman-api-AWS

# Run gunicorn server with the specified configuration file
CMD ["sh", "gunicorn.sh"]
