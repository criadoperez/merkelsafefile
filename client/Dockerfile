# Use an official Python runtime as a parent image
FROM python:3.12-bullseye

# Set the working directory in the container to /app
WORKDIR /app

# Copy the client script and common utilities into the container at /app
COPY ./client/client.py /app/client/
COPY ./common /app/common

# Install the requests library and any other necessary Python packages
RUN pip install requests

# Define environment variables for server URLs
ENV SERVER_URL=http://server:5000/upload
ENV SERVER_REQUEST_URL=http://server:5000/request_file

# The client is intended to be run with command line arguments, so we don't specify a CMD.

