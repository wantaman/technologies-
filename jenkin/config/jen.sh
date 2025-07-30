# !/usr/bin/env bash
set -e

: "${JENKINS_UID:?Environment variable JENKINS_UID is required}"
: "${JENKINS_GID:?Environment variable JENKINS_GID is required}"

# jenkins user requires valid UID:GID permissions at the host level to persist data
usermod -u ${JENKINS_UID} jenkins
groupmod -g ${JENKINS_GID} jenkins
# update ownership of directories (as root)
{
  chown -R jenkins:jenkins /var/jenkins_home
  chown -R jenkins:jenkins /usr/share/jenkins/ref
} ||
{
  echo "[ERROR] Failed 'chown -R jenkins:jenkins ...' command"
}

# allow jenkins to run sudo docker (as root)
echo "jenkins ALL=(root) NOPASSWD: /usr/bin/docker" > /etc/sudoers.d/jenkins
chmod 0440 /etc/sudoers.d/jenkins

# Fix potential PATH issues and ensure java is invoked correctly
JAVA_PATH="$(which java)"
sed -i "s# exec java# exec ${JAVA_PATH}#g" /usr/local/bin/jenkins.sh

# Run Jenkins as jenkins user
exec su jenkins -c "cd ~ && /usr/local/bin/jenkins.sh"
