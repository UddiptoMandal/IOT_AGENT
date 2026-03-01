from pydantic import BaseModel
from typing import Optional, List

class SitesInput(BaseModel):
    pass

class AssetsInput(BaseModel):
    site_name: str

class SensorsInput(BaseModel):
    site_name: str
    asset_id: str

class HistoryInput(BaseModel):
    site_name: str
    asset_id: str
    start: str
    final: str
    sensor_list: Optional[List[str]] = None

class CurrentTimeInput(BaseModel):
    pass