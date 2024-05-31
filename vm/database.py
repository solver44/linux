from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./configs.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Config(Base):
    __tablename__ = "configs"
    id = Column(Integer, primary_key=True, index=True)
    rabbitmq_host = Column(String, index=True)
    rabbitmq_queue = Column(String, index=True)
    kafka_bootstrap_servers = Column(String, index=True)
    kafka_topic = Column(String, index=True)
    redis_host = Column(String, index=True)
    redis_port = Column(Integer, index=True)
    app_name = Column(String, index=True)
    app_type = Column(String, index=True)

Base.metadata.create_all(bind=engine)