# Use an official Python runtime as the parent image
FROM python:3.11.1-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update &&  \
    apt-get install -y --no-install-recommends gcc libpq-dev &&  \
    apt-get clean &&  \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY .. ./
RUN pip install --upgrade pip
## Install required Python libraries
RUN pip install -r requirements.txt

RUN chmod +x /app/run.sh

# Specify the command to run on container start

CMD ["bash", "run.sh"]
