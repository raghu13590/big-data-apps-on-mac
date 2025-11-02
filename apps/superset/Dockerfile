
# Licensed to the Apache Software Foundation (ASF) under one or more contributor license agreements.

FROM big-data-base:latest

# Use bash shell for all RUN commands with pipefail option
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Superset-specific dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends redis-server postgresql postgresql-contrib gosu \
    build-essential libpq-dev libssl-dev libffi-dev libxml2-dev libxslt1-dev \
    libbz2-dev libzstd-dev libsnappy-dev liblz4-dev libkrb5-dev libpam0g-dev \
    gcc g++ make pkg-config git && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Python dependencies
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install apache-superset==2.1.3 pinotdb psycopg2-binary redis "Flask<2.3" marshmallow_enum

ARG SUPERSET_USER=superset
ENV SUPERSET_USER=${SUPERSET_USER}
ENV FLASK_APP=superset

RUN useradd -ms /bin/bash ${SUPERSET_USER} && \
    mkdir -p /var/lib/postgresql /var/run/postgresql /etc/redis /var/lib/redis && \
    chown -R ${SUPERSET_USER}:${SUPERSET_USER} /var/lib/postgresql /var/run/postgresql /etc/redis /var/lib/redis && \
    chmod 640 /etc/ssl/private/ssl-cert-snakeoil.key || true

RUN chown -R postgres:postgres /etc/postgresql /var/lib/postgresql /var/run/postgresql

RUN chown postgres:postgres /etc/ssl/private/ssl-cert-snakeoil.key && \
    chmod 600 /etc/ssl/private/ssl-cert-snakeoil.key

RUN mkdir -p /var/log/postgresql && \
    chown -R postgres:postgres /var/log/postgresql

RUN usermod -aG postgres ${SUPERSET_USER}

COPY --chown=${SUPERSET_USER}:${SUPERSET_USER} entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER root
WORKDIR /

ENV START_REDIS=true
ENV START_POSTGRES=true

ENTRYPOINT ["/entrypoint.sh"]
