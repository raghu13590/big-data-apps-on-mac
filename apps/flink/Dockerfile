# Dockerfile for Flink Cluster

# Use the custom base image built from apps/Dockerfile
FROM big-data-base:latest


# Set environment variables
ARG FLINK_VERSION
ARG FLINK_HOME
ARG FLINK_LIB_PATH
ARG SCALA_VERSION
ARG HADOOP_VERSION
ARG HADOOP_HOME
ARG HADOOP_CONF_DIR
ARG HADOOP_USER_NAME

ENV FLINK_VERSION=${FLINK_VERSION}
ENV FLINK_HOME=${FLINK_HOME}
ENV FLINK_LIB_PATH=${FLINK_LIB_PATH}
ENV SCALA_VERSION=${SCALA_VERSION}
ENV HADOOP_VERSION=${HADOOP_VERSION}
ENV HADOOP_HOME=${HADOOP_HOME}
ENV YARN_CONF_DIR=${HADOOP_CONF_DIR}
ENV HADOOP_USER_NAME=${HADOOP_USER_NAME}
ENV PATH="${PATH}:${HADOOP_HOME}/bin:${FLINK_HOME}/bin"

# exit if any of the variables are not set
RUN missing=""; \
    for var in FLINK_VERSION SCALA_VERSION HADOOP_VERSION HADOOP_USER_NAME FLINK_HOME HADOOP_HOME FLINK_LIB_PATH; do \
        if [ -z "${!var}" ]; then missing="$missing\n - $var"; fi; \
    done; \
    if [ -n "$missing" ]; then \
        echo -e "Error: The following build arguments are not set:$missing"; exit 1; \
    fi

# Switch to root to install packages
USER root

# Download and extract Flink distribution using build args
RUN wget https://archive.apache.org/dist/flink/flink-${FLINK_VERSION}/flink-${FLINK_VERSION}-bin-scala_${SCALA_VERSION}.tgz -O /tmp/flink.tgz && \
    mkdir -p /opt/flink && \
    tar -xzf /tmp/flink.tgz -C /opt && \
    mv /opt/flink-${FLINK_VERSION}/* /opt/flink/ && \
    rm -rf /opt/flink-${FLINK_VERSION} /tmp/flink.tgz

# Install Hadoop
RUN wget https://downloads.apache.org/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz && \
    tar -xzf hadoop-${HADOOP_VERSION}.tar.gz -C /opt && \
    rm hadoop-${HADOOP_VERSION}.tar.gz

# Add Flink Hadoop integration
RUN mkdir -p ${FLINK_LIB_PATH} && \
    wget https://repo1.maven.org/maven2/org/apache/flink/flink-shaded-hadoop-2-uber/2.8.3-10.0/flink-shaded-hadoop-2-uber-2.8.3-10.0.jar -O ${FLINK_LIB_PATH}/flink-shaded-hadoop-2-uber-2.8.3-10.0.jar

RUN wget https://repo1.maven.org/maven2/org/apache/flink/flink-connector-files/1.17.0/flink-connector-files-1.17.0.jar -O ${FLINK_LIB_PATH}/flink-connector-files-1.17.0.jar

# Create hadoop user and set up permissions
RUN groupadd ${HADOOP_USER_NAME} && \
    useradd -m -s /bin/bash -g ${HADOOP_USER_NAME} ${HADOOP_USER_NAME} && \
    usermod -aG sudo ${HADOOP_USER_NAME} && \
    echo "${HADOOP_USER_NAME} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && \
    mkdir -p /tmp/flink-yarn-tmp && \
    mkdir -p ${HADOOP_HOME}/logs && \
    mkdir -p ${FLINK_HOME}/conf && \
    mkdir -p ${FLINK_HOME}/log && \
    mkdir -p /tmp/flink && \
    chmod -R 777 /tmp/flink-yarn-tmp && \
    chmod -R 777 ${HADOOP_HOME}/logs && \
    chmod -R 777 ${FLINK_HOME}/conf && \
    chmod -R 777 ${FLINK_HOME}/log && \
    chmod -R 777 /tmp/flink && \
    chown -R ${HADOOP_USER_NAME}:${HADOOP_USER_NAME} ${FLINK_HOME} && \
    chown -R ${HADOOP_USER_NAME}:${HADOOP_USER_NAME} ${HADOOP_HOME} && \
    chown -R ${HADOOP_USER_NAME}:${HADOOP_USER_NAME} /tmp/flink

# Expose ports for Flink UI and JobManager RPC
EXPOSE 8081 6123 6124

# Copy entrypoint script
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]