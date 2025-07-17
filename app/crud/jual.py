from sqlalchemy.orm import Session
from models import sampah as models_sampah, penjualan as models_penjualan, harga_satuan as models_harga

def create_penjualan(db: Session, sampah_id: int, berat: float, pembeli_id: int):

    # 1. Select tipe_sampah
    sampah = db.query(models_sampah.Sampah).filter_by(sampah_id=sampah_id).first()
    if not sampah:
        raise ValueError("Sampah tidak ditemukan")

    tipe_sampah = sampah.tipe_sampah

    # 2. Calculate harga jual
    harga = db.query(models_harga.HargaSatuan).filter_by(tipe_sampah=tipe_sampah).first()
    if not harga:
        raise ValueError("Harga sampah tidak ditemukan")

    harga_jual = harga.satuan_jual * berat

    # 3. Add to penjualan
    penjualan = models_penjualan.Penjualan(
        pembeli_id=pembeli_id,
        sampah_id=sampah.sampah_id,
        harga_jual=harga_jual
    )
    db.add(penjualan)

    # 4. Set to sold
    sampah.is_sold = True
    
    # Will refresh the penjualan table
    db.commit()
    db.refresh(penjualan)

    return penjualan