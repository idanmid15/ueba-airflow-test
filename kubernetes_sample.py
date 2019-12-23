from airflow import DAG
from datetime import datetime, timedelta
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.operators.dummy_operator import DummyOperator


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2019, 1, 1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'kubernetes_sample', default_args=default_args, schedule_interval=timedelta(minutes=10))


start = DummyOperator(task_id='run_this_first', dag=dag)

passing = KubernetesPodOperator(namespace='airflow',
                          image="python:3.6-alpine3.9",
                          cmds=["python","-c"],
                          arguments=["print('hello world')"],
                          labels={"foo": "bar"},
                          in_cluster=True,
                          name="passing-test",
                          task_id="passing-task",
                          get_logs=True,
                          dag=dag)

#failing = KubernetesPodOperator(namespace='airflow',
#                          image="alpine:3.9",
#                          cmds=["python","-c"],
#                          in_cluster=True,
#                          arguments=["print('hello world')"],
#                          labels={"foo": "bar"},
#                          name="fail",
#                          task_id="failing-task",
#                          get_logs=True,
#                          dag=dag)

passing.set_upstream(start)
#failing.set_upstream(start)
