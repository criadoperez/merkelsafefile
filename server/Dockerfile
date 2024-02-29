# Use an official Python runtime as a parent image
FROM python:3.12-bullseye

# Set the working directory in the container to /app
WORKDIR /app

# Copy the server script and common utilities into the container at /app
COPY ./server/server.py /app/server/
COPY ./common /app/common

# Install Flask and any other necessary Python packages
# You might need to create a requirements.txt file that includes Flask and any other dependencies
RUN pip install Flask

# Create a directory within the container to store uploaded files
RUN mkdir /app/server/server_uploaded_files

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable to store the location of uploaded files
ENV FILE_STORAGE_PATH=/app/server/server_uploaded_files

# Run server.py when the container launches
CMD ["python", "server/server.py"]
