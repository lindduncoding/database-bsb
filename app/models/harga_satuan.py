from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from config import Base

class HargaSatuan(Base):
    __tablename__ = "harga_satuan"

    tipe_sampah = Column(Integer, primary_key=True, index=True)
    nama_sampah = Column(String, unique=True, nullable=False)
    satuan_beli = Column(Integer, nullable=False)
    satuan_jual = Column(Integer, nullable=False)
