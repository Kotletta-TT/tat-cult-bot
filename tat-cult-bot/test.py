from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Facts(Base):
    __tablename__ = 'facts'
    facts = Column(String(3000), primary_key=True)
    key_words = Column(String(100))
    image = Column(String(500))

    def __init__(self, key_words, facts, image):
        self.key_words = key_words
        self.facts = facts
        self.image = image

#
# class Tag(Base):
#     __tablename__ = 'tags'
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String(255), unique=True, nullable=False)
#
#     def __repr__(self):
#         return "<Tag (name='%s')>" % (self.name)
#
#
# # connection
# engine = create_engine('sqlite:///test.db')
#
# # create metadata
# Base.metadata.create_all(engine)
#
# # create session
# Session = sessionmaker(bind=engine)
# session = Session()
#
# # insert data
# tag_cool = Tag(name='cool')
# tag_car = Tag(name='car')
# tag_animal = Tag(name='animal')
#
# session.add_all([tag_animal, tag_car, tag_cool])
# session.commit()
#
# # query data
# t1 = session.query(Tag).filter(Tag.name == 'cool').first()
#
# # update entity
# t1.name = 'cool-up'
# session.commit()
#
# # delete
# session.delete(t1)
# session.commit()
# import datetime
# import json
#
# event = {"bert": "test", "time": [datetime.datetime.now(), datetime.datetime.now()]}
#
# # event = json.dumps(event)
#
# # event = (event)
# test = event.pop("time", None)
#
# for i in range(len(test)):
#     print(i)


