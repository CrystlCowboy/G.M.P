# Use a base image
FROM python:3.8

# Set the working directory
WORKDIR /app

# Copy the application files to the container
COPY . /app

# Install any dependencies
RUN pip install -r requirements.txt

# Define the command to run the application
CMD ["python", "Main.py"]