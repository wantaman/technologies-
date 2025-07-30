FROM jenkins/jenkins:lts

# add ability to run docker from within jenkins (docker in docker)
USER root

# Install Docker CLI inside container
RUN apt-get update && apt-get install -y \
    lsb-release \
    sudo \
    curl \
    gnupg && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | \
    gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] \
      https://download.docker.com/linux/debian $(lsb_release -cs) stable" \
      > /etc/apt/sources.list.d/docker.list && \
    apt-get update && apt-get install -y docker-ce-cli && \
    apt-get install -y file && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# set default user attributes
ENV JENKINS_UID=1000
ENV JENKINS_GID=1000

# create user and add to docker group
RUN groupadd -g 984 docker && usermod -aG docker jenkins

#RUN id jenkins || (echo "User jenkins not found!" && exit 1)

# add entrypoint script
COPY jen.sh /jen.sh
RUN chmod +x /jen.sh

# set default users
#USER jenkins

# bypass normal entrypoint and use custom one
ENTRYPOINT ["/usr/bin/tini", "--", "/jen.sh"]
