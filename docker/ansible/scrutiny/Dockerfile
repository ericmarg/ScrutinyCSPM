FROM nikolaik/python-nodejs:python3.11-nodejs20

# Install Git and necessary dependencies
RUN apt-get update && \
    apt-get install -y git libonig-dev && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /scrutinycspm

# Copy the project files to the working directory
COPY ../../../. .

# Create a virtual environment
RUN python3 -m venv venv

# Activate the virtual environment
ENV PATH="/scrutinycspm/venv/bin:$PATH"

# Install the project dependencies inside the virtual environment
RUN pip install --no-cache-dir setuptools && pip install --no-cache-dir -e .

# Set the working directory
WORKDIR /scrutinycspm/frontend

# Install frontend dependencies
RUN npm install

# Build the frontend
RUN npm run build

EXPOSE 3000

# Set the default command to run the main script
CMD ["npm", "start"]