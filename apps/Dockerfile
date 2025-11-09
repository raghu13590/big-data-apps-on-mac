# Base Dockerfile

FROM ubuntu:focal

# Parameterized build arguments
ARG JAVA_HOME
ARG JDK
ARG PYTHON_VERSION
ARG TZ
ARG LANG
ARG LANGUAGE
ARG LC_ALL

# Set environment variables for runtime
ENV JAVA_HOME=${JAVA_HOME}
ENV JDK=${JDK}
ENV PYTHON_VERSION=${PYTHON_VERSION}
ENV TZ=${TZ}
ENV LANG=${LANG}
ENV LANGUAGE=${LANGUAGE}
ENV LC_ALL=${LC_ALL}
ENV PATH=$JAVA_HOME/bin:$PATH

# Use bash shell for all RUN commands with pipefail option
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Install core system packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        wget \
        curl \
        ca-certificates \
        gnupg \
        software-properties-common \
        lsb-release \
        netcat \
        net-tools \
        less \
        nano \
        vim \
        procps \
        locales && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# --- Java ---
RUN apt-get update && \
    apt-get install -y --no-install-recommends ${JDK} && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# --- Python ---
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python${PYTHON_VERSION} \
        python${PYTHON_VERSION}-pip \
        python${PYTHON_VERSION}-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Set up locale
RUN echo "${LANG} UTF-8" > /etc/locale.gen && \
    locale-gen ${LANG}

# Set timezone
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Create a common directory structure
RUN mkdir -p /opt/app /opt/configs /opt/data /opt/logs

WORKDIR /opt/app

CMD ["/bin/bash"]