import requests
import json
import logging
from datetime import datetime

# Configura o logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GraphAPI:
    def __init__(self, fb_api_token):
        self.base_url = 'https://graph.facebook.com/v22.0/'
        self.api_fields = ['spend', 'cpc', 'cpm', 'objective', 'adset_name',
                           'adset_id', 'clicks', 'campaign_name', 'campaign_id',
                           'conversions', 'frequency', 'conversion_values',
                           'ad_name', 'ad_id']
        self.token = '&access_token=' + fb_api_token


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