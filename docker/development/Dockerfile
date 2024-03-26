FROM ubuntu:latest

# Install Python and necessary dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip git && \
    rm -rf /var/lib/apt/lists/* && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    pip3 install setuptools

ENV PYTHONPATH=/scrutinycspm:/scrutinycspm/src:/scrutinycspm/cli

WORKDIR /scrutinycspm

COPY setup.py .
COPY . .

RUN pip3 install --no-cache-dir -e .
EXPOSE 5678