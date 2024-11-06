FROM apache/airflow:2.10.2

USER root

# Install telnet
RUN apt-get update \
    && apt-get install -y telnet \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow