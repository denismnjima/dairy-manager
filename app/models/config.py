from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError

try:
    engine = create_engine('postgresql://postgres:pass@localhost:5432/dairy_management')
    print("Database engine initialized successfully.")
except SQLAlchemyError as e:
    print(f'Error during engine initialization: {e}')

try:
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    print("Session factory created successfully.")
except SQLAlchemyError as e:
    print(f'Error during session factory creation: {e}')

Base = declarative_base()

def initialize_db():
    import models
    try:
        Base.metadata.create_all(engine)
        print("Database tables created successfully.")
    except SQLAlchemyError as e:
        print(f'Error during table creation: {e}')

