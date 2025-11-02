# Base Dockerfile for Big Data Services
# This image provides common dependencies and configurations for all Java-based big data services
# Services: Hadoop, Spark, Kafka, Pinot, Superset (and others)

FROM ubuntu:focal

# Use bash shell for all RUN commands with pipefail option
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Build arguments with defaults
ARG TZ=UTC
ARG LANG=en_US.UTF-8
ARG LANGUAGE=en_US:en
ARG LC_ALL=en_US.UTF-8
ARG PYTHONIOENCODING=utf-8

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    TZ=${TZ} \
    LANG=${LANG} \
    LANGUAGE=${LANGUAGE} \
    LC_ALL=${LC_ALL} \
    PYTHONIOENCODING=${PYTHONIOENCODING}

# Disable suggests/recommends to reduce image size and configure timezone
RUN echo 'APT::Install-Recommends "0";' > /etc/apt/apt.conf.d/10disableextras && \
    echo 'APT::Install-Suggests "0";' >> /etc/apt/apt.conf.d/10disableextras && \
    if [ -f "/usr/share/zoneinfo/$TZ" ]; then \
        ln -snf /usr/share/zoneinfo/$TZ /etc/localtime; \
        echo $TZ > /etc/timezone; \
    else \
        ln -snf /usr/share/zoneinfo/UTC /etc/localtime; \
        echo "UTC" > /etc/timezone; \
    fi

# Install common system packages
# These are used across multiple services: hadoop, spark, kafka, pinot, superset
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        # Core utilities
        wget \
        curl \
        ca-certificates \
        gnupg \
        software-properties-common \
        lsb-release \
        # Network tools
        netcat \
        net-tools \
        # Text editors and utilities
        less \
        nano \
        vim \
        # Process management
        procps \
        # Java (OpenJDK 11 is common across most services)
        openjdk-11-jdk \
        # Python (used by many services for utilities and client libraries)
        python3 \
        python3-pip \
        python3-dev \
        locales && \
    # Clean up apt cache to reduce image size
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Set up locale
RUN echo "${LANG} UTF-8" > /etc/locale.gen && \
    locale-gen ${LANG}

# Set Java home (for arm64/aarch64 architecture)
# Note: Adjust path for amd64 if needed: /usr/lib/jvm/java-11-openjdk-amd64
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64
ENV PATH=$JAVA_HOME/bin:$PATH

# Create a common directory structure
RUN mkdir -p /opt/app /opt/configs /opt/data /opt/logs

# Set working directory
WORKDIR /opt/app

# Default command
CMD ["/bin/bash"]
