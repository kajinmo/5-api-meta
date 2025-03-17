from .models import Campaign, Ads  # Importe seus Models
from .schema import CampaignResponse  # Importe seus Schemas
from .extract import GraphAPI  # Importe a classe de extração de dados
from .db import SessionLocal  # Importe a sessão do banco de dados
from datetime import date
import logging

# Configura o logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CampaignController:
    def __init__(self, fb_api_token, ad_acc_id):
        self.fb_api = GraphAPI(fb_api_token)
        self.ad_acc_id = ad_acc_id

    def fetch_and_save_campaigns(self):
        """
        Coleta dados de campanhas da API do Facebook e salva no banco de dados.
        """
        db = SessionLocal()
        try:
            # Coleta dados de campanhas
            campaign_status = self.fb_api.get_campaigns_status(self.ad_acc_id)
            if not campaign_status:
                logger.error("Falha ao coletar dados de status das campanhas.")
                return

            # Processa e salva cada campanha
            for campaign_data in campaign_status.get('data', []):
                if campaign_data['status'] == 'ACTIVE':
                    # Cria um objeto Campaign a partir dos dados da API
                    campaign = Campaign(
                        campaign_id=campaign_data['id'],
                        campaign_name=campaign_data['name'],
                        status=campaign_data['status'],
                        date_start=date.today(),  # Exemplo de data
                        date_stop=date.today()    # Exemplo de data
                    )
                    db.add(campaign)
                    logger.info(f"Campanha {campaign_data['name']} salva com sucesso.")

            db.commit()
        except Exception as e:
            logger.error(f"Erro ao salvar campanhas no banco de dados: {e}")
            db.rollback()
        finally:
            db.close()

    def get_campaign_by_id(self, campaign_id: int):
        """
        Busca uma campanha no banco de dados pelo ID.
        """
        db = SessionLocal()
        try:
            campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
            if not campaign:
                logger.error(f"Campanha com ID {campaign_id} não encontrada.")
                return None
            return CampaignResponse.from_orm(campaign)  # Converte o Model para o Schema
        except Exception as e:
            logger.error(f"Erro ao buscar campanha: {e}")
            return None
        finally:
            db.close()