##########################################################
## Description: The fetch_wfs_DAG is a chained sequence of tasks that fetches geospatial feature data from a provided url,
##              transforms it as a JSON format and loads the output to a datalake on S3
##########################################################
## Project: BMI Thünen Institute Breedfides
## Date: 26.10.2023
## Status: prod/dev
##########################################################
## Comments:
##########################################################

import sys
import os
sys.path.append(f'{os.path.dirname(os.path.abspath(__file__))}/src/')
import json 
import pendulum
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.transfers.local_to_s3 import LocalFilesystemToS3Operator

from utility import fetch_api

####################
## DAG definition ##
####################
default_args = {
    "owner": "thünen_institute",
    "depends_on_past": False,
    "start_date": pendulum.datetime(2023, 10, 6, tz='UTC'),
    "retries": 1,
    "retry_delay": timedelta(minutes=3)
}

dag = DAG(
    "fetch_wfs",
    default_args=default_args,
    schedule=None,
    catchup=False,
    tags=["BreedFides", "OGC"]
)

with dag:
    extract = PythonOperator(
        task_id='extract',
        python_callable=fetch_api,
        provide_context=True,
        execution_timeout=timedelta(seconds=3600)
    )
    
    # transform = PythonOperator(
    # )
    
    # load = LocalFilesystemToS3Operator(
    #     task_id='load',
    #     filename=,
    #     dest_key=,
    #     dest_bucket=,
    #     aws_conn_id=,
    #     replace=True     
    # )
    
    extract #>> transform >> load
