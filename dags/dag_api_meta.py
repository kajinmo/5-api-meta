from airflow.decorators import dag, task
from datetime import datetime
import os

from include.controller import CampaignController



fb_api_token = os.getenv('AD_ACC_TOKEN')
ad_acc_id = os.getenv('AD_ACC_ID')


@dag(
        dag_id="dados_api_meta",
        description="pipeline para capturar os dados da api meta",
        schedule_interval="* * * * *",
        start_date=datetime(2025,3,16),
        catchup=False
)
def dag_api_meta():
    @task(task_id='coletar_dados_api')
    def task_coletar_dados_api():
        controller = CampaignController(fb_api_token, ad_acc_id)
        controller.fetch_and_save_campaigns()
        return 'hue'

    @task(task_id='salvar_dados_no_db')
    def task_salvar_dados_no_db():
        return 'aeho'

    t1 = task_coletar_dados_api()
    t2 = task_salvar_dados_no_db()

    t1 >> t2

dag_api_meta()