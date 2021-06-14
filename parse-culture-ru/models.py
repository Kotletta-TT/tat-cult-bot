from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from config import SOURCE


class Event(BaseModel):
    site_id: int
    title: str
    event_source: str = SOURCE
    url: str
    image: Optional[str] = None
    event_date: Optional[str]
    price: int = 0
    currency: str
    agent_name: Optional[str]
    agent_address: Optional[str]
    agent_url: Optional[str]
    event_type: str = None
    event_description: str = None
    gps_latitude: Optional[float]
    gps_longitude: Optional[float]
    tags: Optional[str]
