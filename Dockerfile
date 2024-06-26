# Use a base image compatible with Raspberry Pi (ARM64 architecture)
FROM arm64v8/python:3.8-buster

# Set the working directory
WORKDIR /app

# Copy the application files to the container
COPY . /app

# Install VLC, PulseAudio, and any needed packages specified in requirements.txt
RUN apt-get update && \
    apt-get install -y vlc pulseaudio && \
    apt-get install -y libatlas-base-dev gfortran && \
    pip install --no-cache-dir -r requirements.txt

# Set environment variables for PulseAudio
ENV PULSE_SERVER unix:/run/pulse/native

# Make port 80 available to the world outside this container
EXPOSE 80

# Define the command to run the application
CMD ["python", "Main.py"]

