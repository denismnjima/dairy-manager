from sqlalchemy import Column, Integer, Date, Float, ForeignKey
from config import Base, SessionLocal
from sqlalchemy.orm import relationship
from sqlalchemy.exc import SQLAlchemyError

session = SessionLocal()

class MilkRecord(Base):
    __tablename__ = 'milk_records'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cow_id = Column(Integer, ForeignKey('cows.id'))
    record_date = Column(Date)
    milk_quantity = Column(Float)

    # Relationship back to Cow
    cow = relationship('Cow', back_populates='milk_records')

    @staticmethod
    def show_all_milk_records():
        try:
            return session.query(MilkRecord).all()
        except SQLAlchemyError as error:
            print(error)
            return []

    @staticmethod
    def add_milk_record(cow_id, record_date, milk_quantity):
        try:
            new_record = MilkRecord(cow_id=cow_id, record_date=record_date, milk_quantity=milk_quantity)
            session.add(new_record)
            session.commit()
            session.refresh(new_record)
            return 'success'
        except SQLAlchemyError as error:
            print(error)
            return 'error'

    @staticmethod
    def delete_milk_record(record_id):
        try:
            session.query(MilkRecord).filter(MilkRecord.id == record_id).delete()
            session.commit()
            return 'success'
        except SQLAlchemyError as error:
            print(error)
            return 'error'

    @staticmethod
    def update_milk_record(record_id, milk_quantity):
        try:
            record = session.query(MilkRecord).filter(MilkRecord.id == record_id).first()
            if record:
                record.milk_quantity = milk_quantity
                session.commit()
                return 'success'
            return 'not found'
        except SQLAlchemyError as error:
            print(error)
            return 'error'
