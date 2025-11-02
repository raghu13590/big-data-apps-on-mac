FROM bigdata-base:latest

# Additional environment variables specific to Pinot
ENV PINOT_HOME=/opt/pinot
ENV PATH=$PATH:${PINOT_HOME}/bin
ENV JVM_OPTS="-Xms1G -Xmx4G -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -XX:+UseStringDeduplication"

# Build arguments
ARG PINOT_VERSION
ENV PINOT_VERSION=${PINOT_VERSION}

# Install additional tools needed for Pinot
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
        maven \
        build-essential \
        jq \
        unzip \
        dnsutils \
        iputils-ping && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Download and install Apache Pinot
RUN mkdir -p ${PINOT_HOME} && \
    cd /tmp && \
    wget -q https://archive.apache.org/dist/pinot/apache-pinot-${PINOT_VERSION}/apache-pinot-${PINOT_VERSION}-bin.tar.gz && \
    tar -xzf apache-pinot-${PINOT_VERSION}-bin.tar.gz && \
    mv apache-pinot-${PINOT_VERSION}-bin/* ${PINOT_HOME}/ && \
    rm -rf /tmp/apache-pinot-*

# Download additional plugins and dependencies
RUN cd ${PINOT_HOME}/plugins && \
    wget -q https://repo1.maven.org/maven2/org/apache/pinot/pinot-kafka-2.0/${PINOT_VERSION}/pinot-kafka-2.0-${PINOT_VERSION}-shaded.jar || true && \
    wget -q https://repo1.maven.org/maven2/org/apache/pinot/pinot-s3/${PINOT_VERSION}/pinot-s3-${PINOT_VERSION}-shaded.jar || true && \
    wget -q https://repo1.maven.org/maven2/org/apache/pinot/pinot-avro/${PINOT_VERSION}/pinot-avro-${PINOT_VERSION}-shaded.jar || true

# Create necessary directories with proper permissions
RUN mkdir -p /var/pinot/controller/data \
             /var/pinot/controller/logs \
             /var/pinot/server/data \
             /var/pinot/server/logs \
             /var/pinot/broker/logs \
             /var/pinot/minion/data \
             /var/pinot/minion/logs \
             /opt/pinot/configs \
             /opt/pinot/scripts

# Create non-root user for running services
RUN useradd -ms /bin/bash pinot && \
    chown -R pinot:pinot /var/pinot ${PINOT_HOME}

# Copy entrypoint script
COPY --chown=pinot:pinot entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Switch to pinot user
USER pinot
WORKDIR /home/pinot

ENTRYPOINT ["/entrypoint.sh"]
