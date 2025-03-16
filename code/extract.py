import requests
import json
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os
import logging

from utils import save_data_to_json, save_dataframe_to_csv, save_campaigns_historical_data

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configura o logging
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)  # Cria a pasta de logs se não existir

# Define o nome do arquivo de log com a data atual
log_file = os.path.join(log_dir, f"log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")

# Configura o logging
logging.basicConfig(
    level=logging.INFO,  # Define o nível de log (INFO, WARNING, ERROR, etc.)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Formato das mensagens
    handlers=[
        logging.FileHandler(log_file),  # Salva logs em um arquivo
        logging.StreamHandler()  # Exibe logs no console
    ]
)

logger = logging.getLogger(__name__)

class GraphAPI:
    def __init__(self, fb_api):
        self.base_url = 'https://graph.facebook.com/v22.0/'
        self.api_fields = ['spend', 'cpc', 'cpm', 'objective', 'adset_name',
                           'adset_id', 'clicks', 'campaign_name', 'campaign_id',
                           'conversions', 'frequency', 'conversion_values',
                           'ad_name', 'ad_id']
        self.token = '&access_token=' + fb_api


    def get_insights(self, ad_acc, level='campaign'):
        """
        Coleta dados de insights de uma conta de anúncio do Facebook.

        Args:
            ad_acc (str): ID da conta de anúncio.
            level (str): Nível de agregação dos dados (padrão: 'campaign').

        Returns:
            dict: Dados de insights no formato JSON.
        """
        url = self.base_url + 'act_' + str(ad_acc)
        url += '/insights?level=' + level
        url += '&fields=' + ','.join(self.api_fields)

        try:
            response = requests.get(url + self.token)
            response.raise_for_status()  # Levanta uma exceção para códigos de status 4xx/5xx
            data = response.json()
            logger.info("Dados de insights coletados com sucesso.")
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro na requisição: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao decodificar JSON: {e}")
            return None

        # Processamento dos dados
        for i in data.get('data', []):
            if 'conversions' in i:
                i['conversion'] = float(i['conversions'][0]['value'])

        return data



    def get_campaigns_status(self, ad_acc):
        """
        Coleta informações sobre o status das campanhas de uma conta de anúncio do Facebook.
        Não é possível pegar o status da campanha pela função anterior, precisou dessa adicional

        Args:
            ad_acc (str): ID da conta de anúncio.

        Returns:
            dict: Dados de status das campanhas no formato JSON.
                Retorna None em caso de erro.
        """
        url = self.base_url + 'act_' + str(ad_acc)
        url += '/campaigns?fields=name,status,adsets{name, id}'

        try:
            # Faz a requisição com timeout de 10 segundos
            response = requests.get(url + self.token, timeout=10)
            response.raise_for_status()  # Levanta exceção para códigos de status 4xx/5xx
            data = response.json()
            logger.info("Dados de status das campanhas coletados com sucesso.")
        except requests.exceptions.Timeout:
            logger.error("A requisição excedeu o tempo limite.")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro na requisição: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao decodificar JSON: {e}")
            return None

        return data



    def get_adset_status(self, ad_acc):
        """
        Coleta informações sobre o status dos conjuntos de anúncios (adsets) de uma conta de anúncio do Facebook.

        Args:
            ad_acc (str): ID da conta de anúncio.

        Returns:
            dict: Dados de status dos conjuntos de anúncios no formato JSON.
                Retorna None em caso de erro.
        """  
        
        url = self.base_url + 'act_' + str(ad_acc)
        url += '/adsets?fields=name,status,id'
        
        try:
            # Faz a requisição com timeout de 10 segundos
            response = requests.get(url + self.token, timeout=10)
            response.raise_for_status()  # Levanta exceção para códigos de status 4xx/5xx
            data = response.json()
            logger.info("Dados de status dos conjuntos de anúncios coletados com sucesso.")
        except requests.exceptions.Timeout:
            logger.error("A requisição excedeu o tempo limite.")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro na requisição: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao decodificar JSON: {e}")
            return None

        return data
    

    def get_data_over_time(self, campaign):
        """
        Coleta dados históricos de uma campanha ao longo do tempo.

        Args:
            campaign (str): ID da campanha.

        Returns:
            dict: Dados históricos da campanha no formato JSON.
                Retorna None em caso de erro.
        """
        url = self.base_url + str(campaign)
        url += '/insights?fields=' + ','.join(self.api_fields)
        url += '&date_preset=last_30d&time_increment=1'

        try:
            # Faz a requisição com timeout de 10 segundos
            response = requests.get(url + self.token, timeout=10)
            response.raise_for_status()  # Levanta exceção para códigos de status 4xx/5xx
            data = response.json()
            logger.info(f"Dados históricos da campanha {campaign} coletados com sucesso.")
        except requests.exceptions.Timeout:
            logger.error("A requisição excedeu o tempo limite.")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro na requisição: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao decodificar JSON: {e}")
            return None

        # Processamento dos dados
        for i in data.get('data', []):
            if 'conversions' in i:
                i['conversion'] = float(i['conversions'][0]['value'])

        return data


if __name__ == '__main__':
    fb_api = os.getenv('AD_ACC_TOKEN')
    ad_acc = os.getenv('AD_ACC_ID')
   
    self = GraphAPI(fb_api)

    # Coleta o status das campanhas
    campaign_status = self.get_campaigns_status(ad_acc)
    if campaign_status:
        save_data_to_json(campaign_status, 'campaign_status')
        logger.info("Dados de status das campanhas salvos com sucesso.")
    else:
        logger.error("Falha ao coletar dados de status das campanhas.")

     # Coleta o status dos conjuntos de anúncios
    adset_status = self.get_adset_status(ad_acc)
    if adset_status:
        save_data_to_json(adset_status, 'adset_status')
        logger.info("Dados de status dos conjuntos de anúncios salvos com sucesso.")
    else:
        logger.error("Falha ao coletar dados de status dos conjuntos de anúncios.")

    # Coleta dados históricos das campanhas ativas
    campaign_ids = [campaign['id'] for campaign in campaign_status['data'] if campaign['status'] == 'ACTIVE']
    df_campaigns = save_campaigns_historical_data(self, campaign_ids)
    if df_campaigns is not None:
        save_dataframe_to_csv(df_campaigns, 'campaigns_historical_data')
        logger.info("Dados históricos das campanhas salvos com sucesso.")
    else:
        logger.error("Falha ao coletar dados históricos das campanhas.")