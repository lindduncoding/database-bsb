from sqlalchemy import Column, Integer, String
from config import Base

class Nasabah(Base):
    __tablename__ = "nasabah"

    nasabah_id = Column(Integer, primary_key=True, index=True)
    nama = Column(String, unique=True, nullable=False)
    nomor_rekening = Column(String, unique=True, nullable=False)
