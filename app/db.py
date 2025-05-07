from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create a connection to a SQLite database
# ':memory:' creates an in-memory database, or use a file path like 'sqlite:///database.db'
engine = create_engine('sqlite:///database.db', echo=True)

# Create a base class for declarative class definitions
Base = declarative_base()

# Create a session factory
Session = sessionmaker(bind=engine)

class Shipment(Base):
    __tablename__ = 'shipment'

    id = Column(String, primary_key=True)
    origin = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    status = Column(String, nullable=False)

class SensorEvent(Base):
    __tablename__ = 'sensorEvents'

    id = Column(Integer, primary_key=True)
    shipment_id = Column(String, ForeignKey('shipment.id'))
    timestamp = Column(DateTime, nullable=False)
    latitude = Column(Integer, nullable=True)
    longitude = Column(Integer, nullable=True)
    temp = Column(Integer, nullable=False)

def init_db():
    print("Initializing database...")
    Base.metadata.create_all(engine)
    print("Initialized")