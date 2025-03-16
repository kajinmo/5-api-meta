import pandas as pd
from datetime import datetime
import os
import json



def save_data_to_json(data_in_dict, dataset_name):
    try:
        data_to_save = data_in_dict['data']

        # Gerar a data e hora atuais no formato dd-mm-yyyy hh-mm
        current_time = datetime.now().strftime('%d-%m-%Y %Hh%M')

        file_name = f'{dataset_name} {current_time}.json'
        subdirectory = "output_json_files"
        file_path = os.path.join(subdirectory, file_name)
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data_to_save, json_file, indent=4, ensure_ascii=False)
            print(f"Dados salvos com sucesso em '{file_path}'")
    except:
        print("Não foi possível salvar {dataset_name}.")



def save_dataframe_to_csv(dataframe, dataset_name):
    try:
        # Gerar a data e hora atuais no formato dd-mm-yyyy hh-mm
        current_time = datetime.now().strftime('%d-%m-%Y %Hh%M')

        file_name = f'{dataset_name} {current_time}.csv'
        subdirectory = "output_csv_files"
        file_path = os.path.join(subdirectory, file_name)
        dataframe.to_csv(file_path, index=False, encoding='utf-8')
        print(f"Dados salvos com sucesso em '{file_path}'")

    except:
        print("Não foi possível salvar {dataset_name}.")



def save_campaigns_historical_data(self, campaign_ids):
    try:
        df_final = pd.DataFrame()
        
        for campaign in campaign_ids:
            campaign_data = self.get_data_over_time(campaign)['data']

            # Converter strings numéricas para float/int
            for entry in campaign_data:
                entry['spend'] = float(entry['spend'])
                entry['cpc'] = float(entry['cpc'])
                entry['cpm'] = float(entry['cpm'])
                entry['clicks'] = int(entry['clicks'])
                entry['frequency'] = float(entry['frequency'])

            # Criar um DataFrame (estrutura tabular)
            df_campaign = pd.DataFrame(campaign_data)
            df_final = pd.concat([df_final, df_campaign], ignore_index=True)
            
        return df_final
     
    except:
        print("Não foi possível salvar os dados históricos das campanhas.")