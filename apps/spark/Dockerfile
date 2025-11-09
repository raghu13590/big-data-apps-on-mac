# Dockerfile for Spark Cluster

# Use the base Dockerfile
FROM big-data-base:latest

# Set the Spark and Hadoop versions
ARG HADOOP_VERSION
ARG HADOOP_HOME
ARG HADOOP_CONF_DIR
ARG SPARK_VERSION
ARG SPARK_HADOOP_VERSION
ARG SPARK_HOME

ENV HADOOP_VERSION=${HADOOP_VERSION}
ENV HADOOP_HOME=${HADOOP_HOME}
ENV HADOOP_CONF_DIR=${HADOOP_CONF_DIR}
ENV SPARK_VERSION=${SPARK_VERSION}
ENV SPARK_HADOOP_VERSION=${SPARK_HADOOP_VERSION}
ENV SPARK_HOME=${SPARK_HOME}

# Download and extract glibc source files
RUN wget https://ftp.gnu.org/gnu/glibc/glibc-2.36.tar.gz && \
    tar -xzf glibc-2.36.tar.gz -C /opt && \
    rm glibc-2.36.tar.gz

# Compile the C source files
# WORKDIR /opt/glibc-2.36
# RUN mkdir build && cd build && ../configure --disable-sanity-checks && make

RUN echo "spark verison is ${SPARK_VERSION} and spark hadoop version is ${SPARK_HADOOP_VERSION} and hadoop version is ${HADOOP_VERSION} and hadoop home is ${HADOOP_HOME}"

# Install Spark
RUN wget https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${SPARK_HADOOP_VERSION}.tgz && \
    tar -xzf spark-${SPARK_VERSION}-bin-hadoop${SPARK_HADOOP_VERSION}.tgz -C /opt && \
    mv /opt/spark-${SPARK_VERSION}-bin-hadoop${SPARK_HADOOP_VERSION} /opt/spark && \
    rm spark-${SPARK_VERSION}-bin-hadoop${SPARK_HADOOP_VERSION}.tgz

# Install Hadoop binaries
RUN wget https://downloads.apache.org/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz \
    && tar -xzf hadoop-${HADOOP_VERSION}.tar.gz -C /opt \
    && rm hadoop-${HADOOP_VERSION}.tar.gz

# install pyspark
RUN pip3 install pyspark

# Set environment variables
ENV SPARK_HOME=${SPARK_HOME}
ENV HADOOP_CONF_DIR=${HADOOP_CONF_DIR}
ENV PATH=$PATH:$SPARK_HOME/bin:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

# Copy entrypoint script
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Expose ports for Spark UI
EXPOSE 8082 8083 8084 7077 18080

# Set the entrypoint script
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]