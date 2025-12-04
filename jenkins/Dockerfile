FROM jenkins/jenkins:lts

USER root

# Install Docker, Node.js 20, Python3 with pip & venv
RUN apt-get update && \
    apt-get install -y curl wget git python3 python3-pip python3-venv && \
    \
    # Install Docker
    curl -fsSL https://get.docker.com | sh && \
    \
    # Install Node.js 20 LTS (includes npm)
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g npm@latest && \
    \
    # Add jenkins to docker group (so Jenkins can run Docker)
    usermod -aG docker jenkins && \
    \
    # Cleanup
    apt-get clean && rm -rf /var/lib/apt/lists/*

USER jenkins
