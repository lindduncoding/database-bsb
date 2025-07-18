from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from config import Base
from datetime import datetime
from sqlalchemy.orm import relationship

class Pembelian(Base):
    __tablename__ = "pembelian"

    beli_id = Column(Integer, primary_key=True, index=True)
    no_invoice = Column(String, unique=True, index=True)
    nasabah_id = Column(Integer, ForeignKey("nasabah.nasabah_id"), nullable=False)
    sampah_id = Column(Integer, ForeignKey("sampah.sampah_id"), nullable=False)
    harga_beli = Column(Float, nullable=False)
    tanggal_beli = Column(DateTime, default=datetime.now, nullable=False)
    berat = Column(Float, nullable=False, default=1)

    nasabah = relationship("Nasabah")
    sampah = relationship("Sampah")
