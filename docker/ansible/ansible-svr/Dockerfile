FROM python

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ssh \
    sshpass

# Install Ansible and other Python dependencies
RUN pip install --no-cache-dir \
    ansible \
    ansible-lint \
    yamllint

# Set the working directory
WORKDIR /ansible

# Copy any necessary files or directories into the image
# COPY . /ansible

# Set any environment variables if needed
ENV ANSIBLE_HOST_KEY_CHECKING=False

# Specify the command to run when the container starts
CMD ["tail", "-f", "/dev/null"]