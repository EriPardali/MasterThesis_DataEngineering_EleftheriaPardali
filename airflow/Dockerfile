FROM apache/airflow:2.9.3

USER root
RUN apt-get update && apt-get install -y gcc libpq-dev && apt-get clean

USER airflow

COPY requirements.txt /opt/airflow/requirements.txt
RUN pip install --no-cache-dir \
    -r /opt/airflow/requirements.txt \
    --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.9.3/constraints-3.10.txt"
