from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from config import Base
from datetime import datetime

class Penjualan(Base):
    __tablename__ = "penjualan"

    jual_id = Column(Integer, primary_key=True, index=True)
    no_invoice = Column(String, unique=True, index=True)
    pembeli_id = Column(Integer, ForeignKey("pembeli.pembeli_id"), nullable=False)
    sampah_id = Column(Integer, ForeignKey("sampah.sampah_id"), nullable=False)
    harga_jual = Column(Float, nullable=False)
    tanggal_jual = Column(DateTime, default=datetime.now, nullable=False)
    berat = Column(Float, nullable=False, default=1)

    # Python level relationship, not SQL level
    # Abstract SQL relationship even more, easier for OOP
    pembeli = relationship("Pembeli")
    sampah = relationship("Sampah")
