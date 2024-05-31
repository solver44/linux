#!/bin/bash

# Update package information, ensure that APT works with the https method, and that CA certificates are installed.
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common

# Add the Docker repository GPG key to your system.
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# Add the Docker repository to APT sources.
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

# Update your package database with Docker packages from the newly added repo.
sudo apt-get update

# Install Docker.
sudo apt-get install -y docker-ce

# Ensure Docker is running.
sudo systemctl status docker

# Install Docker Compose.
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation.
docker --version
docker-compose --version

docker-compose up --build