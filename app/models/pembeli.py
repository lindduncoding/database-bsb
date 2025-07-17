from sqlalchemy import Column, Integer, String
from config import Base

class Pembeli(Base):
    __tablename__ = "pembeli"

    pembeli_id = Column(Integer, primary_key=True, index=True)
    nama = Column(String, unique=True, nullable=False)
    nomor_pembeli = Column(String, unique=True, nullable=False)
