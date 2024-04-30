FROM python

# Install Ansible and any required Python dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ansible \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /ansible

# Copy requirements.txt if needed and install Python dependencies
# COPY requirements.txt .
# RUN pip install -r requirements.txt

# Expose any ports if needed
EXPOSE 8080

# Start any default command if needed
# CMD ["ansible-playbook", "playbook.yml"]
