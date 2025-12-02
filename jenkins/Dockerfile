FROM jenkins/jenkins:lts

USER root

# Install Python3 + pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip

# Install Node.js (v18 LTS)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs

# Install Docker CLI
RUN apt-get install -y docker.io && \
    usermod -aG docker jenkins

USER jenkins
