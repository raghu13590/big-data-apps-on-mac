FROM big-data-base:latest

# Set environment variables for Kafka
ENV KAFKA_VERSION=3.5.1
ENV KAFKA_HOME=/opt/kafka
ENV PATH=$PATH:$KAFKA_HOME/bin

# Download and install Kafka
RUN wget https://archive.apache.org/dist/kafka/${KAFKA_VERSION}/kafka_2.12-${KAFKA_VERSION}.tgz && \
    tar -xzf kafka_2.12-${KAFKA_VERSION}.tgz -C /opt && \
    mv /opt/kafka_2.12-${KAFKA_VERSION} $KAFKA_HOME && \
    rm kafka_2.12-${KAFKA_VERSION}.tgz

# Expose Kafka port
EXPOSE 9092