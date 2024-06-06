# Use a base image compatible with Raspberry Pi (ARM architecture)
FROM python:3.8-buster

# Set the working directory
WORKDIR /app

# Copy the application files to the container
COPY . /app

# Install dependencies step by step and check for errors
RUN apt-get update && \
    apt-get install -y vlc && \
    apt-get install -y libatlas-base-dev gfortran && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define the command to run the application
CMD ["python", "Main.py"]
