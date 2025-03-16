import requests
import json
import pandas as pd
from dotenv import load_dotenv
import os
from utils import save_data_to_json, save_dataframe_to_csv, save_campaigns_historical_data

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()


class GraphAPI:
    def __init__(self, fb_api):
        self.base_url = 'https://graph.facebook.com/v22.0/'
        self.api_fields = ['spend', 'cpc', 'cpm', 'objective', 'adset_name',
                           'adset_id', 'clicks', 'campaign_name', 'campaign_id',
                           'conversions', 'frequency', 'conversion_values',
                           'ad_name', 'ad_id']
        self.token = '&access_token=' + fb_api


    def get_insights(self, ad_acc, level='campaign'):
        url = self.base_url + 'act_' + str(ad_acc)
        url += '/insights?level=' + level
        url += '&fields=' + ','.join(self.api_fields)

        data = requests.get(url + self.token)
        data = json.loads(data._content.decode('utf-8'))
    

        # conversion é uma list de dicionarios, essa etapa melhora um pouco a leitura
        for i in data['data']:
            if 'conversions' in i:
                i['conversion'] = float(i['conversions'][0]['value'])

        return data
    

    def get_campaigns_status(self, ad_acc):
        '''
        coleta informações de campanhas - não é possível pegar o status da campanha pela função anterior, precisou dessa adicional
        '''
        url = self.base_url + 'act_' + str(ad_acc)
        url += '/campaigns?fields=name,status,adsets{name, id}'
        data = requests.get(url + self.token)
        data =  json.loads(data._content.decode('utf-8'))
        return data


    def get_adset_status(self, ad_acc):
        '''
        coleta informações do conjunto de ads
        '''
        url = self.base_url + 'act_' + str(ad_acc)
        url += '/adsets?fields=name,status,id'
        data = requests.get(url + self.token)
        data =  json.loads(data._content.decode('utf-8'))
        return data
    

    def get_data_over_time(self, campaign):
        '''
        criar histórico: ver como esses dados da campanha se comportaram ao longo do tempo       
        '''
        url = self.base_url + str(campaign)
        url += '/insights?fields=' + ','.join(self.api_fields)
        url += '&date_preset=last_30d&time_increment=1'

        data = requests.get(url + self.token)
        data = json.loads(data._content.decode('utf-8'))
        for i in data['data']:
            if 'conversions' in i:
                i['conversion'] = float(i['conversions'][0]['value'])
        return data



if __name__ == '__main__':
    fb_api = os.getenv('AD_ACC_TOKEN')
    ad_acc = os.getenv('AD_ACC_ID')
   
    self = GraphAPI(fb_api)

    # Salvar o report de insights em json
    insights = self.get_insights(ad_acc)
    save_data_to_json(insights, 'insights')

    # Salvar o report de campaign status em json
    campaign_status = self.get_campaigns_status(ad_acc)
    save_data_to_json(campaign_status, 'campaign_status')

    # Salvar o report de adset status em json
    adset_status = self.get_adset_status(ad_acc)
    save_data_to_json(adset_status, 'adset_status')

    # Extrair todos os IDs das campanhas ATIVAS e salvar em csv
    campaign_ids = [campaign['id'] for campaign in campaign_status['data'] if campaign['status'] == 'ACTIVE']
    df_campaigns = save_campaigns_historical_data(self, campaign_ids)
    save_dataframe_to_csv(df_campaigns, 'campaigns_historical_data')