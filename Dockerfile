# Use a base image
FROM python:3.8

# Set the working directory
WORKDIR /app

# Copy the application files to the container
COPY . /app

# Install VLC and any needed packages specified in requirements.txt
RUN apt-get update && apt-get install -y vlc && pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define the command to run the application
CMD ["python", "Main.py"]