from sqlalchemy import Column,Integer,String,Date,ForeignKey
from db.config import Base
from sqlalchemy.orm import relationship

class HealthRecord(Base):
    __tablename__ = 'health_records'
    id = Column(Integer,primary_key=True, autoincrement=True)
    cow_id = Column(Integer,ForeignKey('cows.id'))
    visit_date = Column(Date)
    description = Column(String(255))
    treatment = Column(String(255))

    cow = relationship('Cow',back_populates='health_records')
