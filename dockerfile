FROM apache/airflow:latest
USER root
RUN apt update && \

    apt install git -y && \

    apt clean
    
USER airflow