# Use the official Python image as the base image
FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Copy your Python script into the container
COPY main.py .

# Expose the port your server listens on
EXPOSE 3000

# Command to run your Python script when the container starts
CMD ["python", "main.py"]
