import datetime as dt
from datetime import timedelta

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

import pandas as pd

def CSVToJson():
    df=pd.read_csv('/home/guilhermeld/data_engineering/code/data.csv')
    for i,r in df.iterrows():
        print(r['name'])
    df.to_json('fromAirflow.JSON',orient='records')

default_args = {
    'owner': 'paulcrickard',
    'start_date': dt.datetime(2022, 3, 25),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5),
}

with DAG('MyCSVDAG',
    default_args=default_args,
    schedule_interval=timedelta(minutes=5),
    # '0 * * * *',
) as dag:
    print_starting = BashOperator(task_id="starting",
        bash_command='echo "I\'m reading the CSV now..."')
    
    CSVJson = PythonOperator(task_id="convertCSVtoJSON", python_callable=CSVToJson)
    print_starting >> CSVJson