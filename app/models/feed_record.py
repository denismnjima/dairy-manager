from sqlalchemy import Column, Integer, String, Date, ForeignKey
from config import Base, SessionLocal
from sqlalchemy.orm import relationship
from sqlalchemy.exc import SQLAlchemyError

session = SessionLocal()

class FeedRecord(Base):
    __tablename__ = 'feed_records'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cow_id = Column(Integer, ForeignKey('cows.id'))
    feed_type = Column(String(100))
    quantity = Column(Integer)
    date = Column(Date)

    # Relationship back to Cow
    cow = relationship('Cow', back_populates='feed_records')  # Ensure this is in place

    @staticmethod
    def show_all_feed_records():
        try:
            return session.query(FeedRecord).all()
        except SQLAlchemyError as error:
            print(error)
            return []

    @staticmethod
    def add_feed_record(cow_id, feed_type, quantity, date):
        try:
            new_record = FeedRecord(cow_id=cow_id, feed_type=feed_type, quantity=quantity, date=date)
            session.add(new_record)
            session.commit()
            session.refresh(new_record)
            return 'success'
        except SQLAlchemyError as error:
            print(error)
            return 'error'

    @staticmethod
    def delete_feed_record(record_id):
        try:
            session.query(FeedRecord).filter(FeedRecord.id == record_id).delete()
            session.commit()
            return 'success'
        except SQLAlchemyError as error:
            print(error)
            return 'error'

    @staticmethod
    def update_feed_record(record_id, feed_type, quantity):
        try:
            record = session.query(FeedRecord).filter(FeedRecord.id == record_id).first()
            if record:
                record.feed_type = feed_type
                record.quantity = quantity
                session.commit()
                return 'success'
            return 'not found'
        except SQLAlchemyError as error:
            print(error)
            return 'error'
