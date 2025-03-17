# o schema do pydantic
from pydantic import BaseModel
from datetime import date

class CampaignCreate(BaseModel):
    spend: float
    cpc: float
    cpm: float
    objective: str
    clicks: int
    campaign_name: str
    campaign_id: str
    frequency: float
    date_start: date
    date_stop: date

    class Config:
        from_attributes = True