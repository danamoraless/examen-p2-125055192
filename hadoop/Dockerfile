FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive

# Java, Python, SSH y utilidades
RUN apt-get update && apt-get install -y --no-install-recommends \
      default-jre-headless python3 \
      openssh-server openssh-client \
      curl ca-certificates procps \
    && rm -rf /var/lib/apt/lists/*

# Variables de entorno
ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV HADOOP_VERSION=3.4.1
ENV HADOOP_HOME=/opt/hadoop
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

# Descargar e instalar Hadoop (modo standalone por defecto)
RUN curl -fsSL https://archive.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz \
      | tar -xz -C /opt \
    && mv /opt/hadoop-${HADOOP_VERSION} ${HADOOP_HOME}

# Hadoop necesita saber JAVA_HOME también en su propia config
RUN echo "export JAVA_HOME=${JAVA_HOME}" >> ${HADOOP_HOME}/etc/hadoop/hadoop-env.sh

# Usuario sin contraseña (solo entra por llave SSH)
RUN useradd -m -s /bin/bash hadoop && usermod -p '*' hadoop

# SSH sin contraseña: llave generada sin passphrase
USER hadoop
RUN mkdir -p /home/hadoop/.ssh \
    && ssh-keygen -t ed25519 -N "" -f /home/hadoop/.ssh/id_ed25519 \
    && cat /home/hadoop/.ssh/id_ed25519.pub >> /home/hadoop/.ssh/authorized_keys \
    && chmod 700 /home/hadoop/.ssh \
    && chmod 600 /home/hadoop/.ssh/authorized_keys \
    && printf "Host *\n  StrictHostKeyChecking no\n  UserKnownHostsFile /dev/null\n" > /home/hadoop/.ssh/config \
    && chmod 600 /home/hadoop/.ssh/config

USER root
RUN mkdir -p /run/sshd /data/input /data/output \
    && chown -R hadoop:hadoop /data

EXPOSE 22

# sshd en primer plano mantiene vivo el contenedor
CMD ["/usr/sbin/sshd", "-D"]