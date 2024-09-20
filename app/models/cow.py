from sqlalchemy import Column, Integer, String, Date
from config import Base, SessionLocal
from sqlalchemy.orm import relationship
from sqlalchemy.exc import SQLAlchemyError

session = SessionLocal()

class Cow(Base):
    __tablename__ = 'cows'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    breed = Column(String(50))
    birth_date = Column(Date)
    tag_number = Column(String(50))

    # Relationships
    milk_records = relationship("MilkRecord", back_populates="cow", cascade="all, delete-orphan")
    feed_records = relationship("FeedRecord", back_populates="cow", cascade="all, delete-orphan")  # <-- Add this

    def add_cows(self):
        try:
            session.add(self)
            session.commit()
            session.refresh(self)
            print('Cow added successfully')
        except SQLAlchemyError as error:
            print(f'Error encountered: {error}')

def delete_cow(cow_id):
    try:
        session.query(Cow).filter(Cow.id == cow_id).delete()
        session.commit()
        return 'success'
    except SQLAlchemyError as error:
        print(error)
        return 'error'

def show_all_cows():
    try:
        return session.query(Cow).all()
    except SQLAlchemyError as error:
        print(error)
        return []
