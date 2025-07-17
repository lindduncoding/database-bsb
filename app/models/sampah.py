from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from config import Base
from sqlalchemy.orm import relationship

class Sampah(Base):
    __tablename__ = "sampah"

    sampah_id = Column(Integer, primary_key=True, index=True)
    tipe_sampah = Column(Integer, ForeignKey("harga_satuan.tipe_sampah"), nullable=False)
    berat = Column(Float, nullable=False)
    is_sold = Column(Boolean, default=False)

    harga_satuan = relationship("HargaSatuan")
