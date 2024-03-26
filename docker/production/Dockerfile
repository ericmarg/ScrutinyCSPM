# Use the official Python base image
FROM python:latest

# Install Git and necessary dependencies
RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /scrutinycspm

# Copy the project files to the working directory
COPY . .

# Install the project dependencies
RUN pip install --no-cache-dir -e .

# Set the default command to run the main script
CMD ["python", "cli/main.py"]