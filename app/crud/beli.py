from sqlalchemy.orm import Session
from models import sampah as models_sampah, pembelian as models_pembelian, harga_satuan as models_harga, nasabah as models_nasabah

def create_pembelian(db: Session, tipe_sampah: int, berat: float, no_rekening: str):

    # 1. Upsert Sampah
    sampah = db.query(models_sampah.Sampah).filter_by(tipe_sampah=tipe_sampah).first()

    if sampah:
        sampah.stok += berat
    else:
        sampah = models_sampah.Sampah(tipe_sampah=tipe_sampah, stok=berat)
        db.add(sampah)
        db.flush()  # To get sampah.id before commit

    # 2. Calculate harga beli
    harga = db.query(models_harga.HargaSatuan).filter_by(tipe_sampah=tipe_sampah).first()
    if not harga:
        raise ValueError("Harga sampah tidak ditemukan")

    harga_beli = harga.satuan_beli * berat

    nasabah = db.query(models_nasabah.Nasabah).filter_by(no_rekening=no_rekening).first()
    nasabah_id = nasabah.nasabah_id

    # 3. Add to pembelian
    pembelian = models_pembelian.Pembelian(
        nasabah_id=nasabah_id,
        sampah_id=sampah.sampah_id,
        berat=berat,
        harga_beli=harga_beli
    )
    db.add(pembelian)
    db.commit()

    # Will refresh the pembelian table
    db.refresh(pembelian)

    return pembelian