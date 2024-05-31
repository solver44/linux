#!/bin/bash

# Update the package repository
sudo apt-get update

# Install prerequisites
sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# Add Docker's official repository
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# Update the package repository again
sudo apt-get update

# Install Docker
sudo apt-get install -y docker-ce

# Verify that Docker is installed correctly
sudo systemctl status docker

# Add your user to the Docker group to avoid using 'sudo' with Docker commands
sudo usermod -aG docker ${USER}

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep -oP '"tag_name": "\K(.*)(?=")')" -o /usr/local/bin/docker-compose

# Apply executable permissions to the Docker Compose binary
sudo chmod +x /usr/local/bin/docker-compose

# Verify that Docker Compose is installed correctly
docker-compose --version

echo "Docker and Docker Compose have been installed successfully."