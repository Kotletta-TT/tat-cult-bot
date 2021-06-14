from sqlalchemy import Column, Integer, String, DateTime, ARRAY, Float, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    site_id = Column(Integer)
    title = Column(String(200))
    event_source = Column(String(400))
    event_date = Column(Text)
    url = Column(String(600))
    image = Column(String(600))
    price = Column(Integer)
    currency = Column(String(10))
    agent_name = Column(String(200))
    agent_address = Column(String(400))
    agent_url = Column(String(200))
    event_type = Column(String(100))
    event_description = Column(String(1000))
    gps_latitude = Column(Float(8))
    gps_longitude = Column(Float(8))
    tags = Column(String(300))

    def __init__(self, site_id, title, event_source, event_date, url, image, price, currency, agent_name, agent_address,
                 agent_url, event_type, event_description, gps_latitude, gps_longitude, tags) -> None:
        self.site_id = site_id
        self.title = title
        self.event_source = event_source
        self.event_date = event_date
        self.url = url
        self.image = image
        self.price = price
        self.currency = currency
        self.agent_name = agent_name
        self.agent_address = agent_address
        self.agent_url = agent_url
        self.event_type = event_type
        self.event_description = event_description
        self.gps_latitude = gps_latitude
        self.gps_longitude = gps_longitude
        self.tags = tags

class Facts(Base):
    __tablename__ = 'facts'
    id = Column(Integer, primary_key=True)
    facts = Column(String(3000))
    key_words = Column(String(100))
    image = Column(String(500))

    def __init__(self, key_words, facts, image):
        self.key_words = key_words
        self.facts = facts
        self.image = image