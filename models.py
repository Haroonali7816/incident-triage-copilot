from sqlalchemy import Column, DateTime, Integer, String,Text, DateTime,JSON
from database import Base

class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)

    #identity from GitHub
    github_id = Column(Integer, unique=True, index=True, nullable = False)
    github_number = Column(Integer, nullable = False)
    html_url = Column(String,nullable = False)

    #Content
    title = Column(String,nullable = False)
    body = Column(Text,nullable = True)
    state = Column(String,nullable = False) # 'open' or 'close'
    labels = Column(JSON,nullable = False, default=list)

#Timestamps
    created_at = Column(DateTime, nullable = False)
    closed_at = Column(DateTime, nullable = True)

    severity = Column(String,nullable =True)
    category = Column(String, nullable = True)
    summary = Column(String, nullable = True)
