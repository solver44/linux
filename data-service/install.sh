#!/bin/bash

# Update package list and install prerequisites
sudo apt-get update
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common

# Add Docker’s official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# Add Docker apt repository
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

# Update package list again
sudo apt-get update

# Install Docker
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Verify Docker installation
docker --version

# Pull RabbitMQ image
docker pull rabbitmq:management

# Run RabbitMQ container with restart always
docker run -d --name rabbitmq \
  --restart always \
  -p 5672:5672 \
  -p 15672:15672 \
  rabbitmq:management

# Pull Kafka image
docker pull wurstmeister/kafka

# Pull Zookeeper image (Kafka dependency)
docker pull wurstmeister/zookeeper

# Run Zookeeper container with restart always
docker run -d --name zookeeper \
  --restart always \
  -p 2181:2181 \
  wurstmeister/zookeeper

# Run Kafka container with restart always
docker run -d --name kafka \
  --restart always \
  --link zookeeper:zookeeper \
  -p 9092:9092 \
  -e KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181 \
  -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 \
  wurstmeister/kafka

# Print status of containers
docker ps

echo "RabbitMQ and Kafka containers are up and running with restart always!"
