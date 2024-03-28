FROM ubuntu:latest

# Install Python and necessary dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv git && \
    rm -rf /var/lib/apt/lists/* && \
    ln -s /usr/bin/python3 /usr/bin/python

ENV PYTHONPATH=/scrutinycspm:/scrutinycspm/src:/scrutinycspm/cli

WORKDIR /scrutinycspm

COPY setup.py .
COPY . .

# Create a virtual environment
RUN python -m venv venv

# Activate the virtual environment
ENV PATH="/scrutinycspm/venv/bin:$PATH"

# Install setuptools and the project dependencies inside the virtual environment
RUN pip install --no-cache-dir setuptools && \
    pip install --no-cache-dir -e .