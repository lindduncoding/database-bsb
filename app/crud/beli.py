from sqlalchemy.orm import Session
from models import sampah as models_sampah, pembelian as models_pembelian, harga_satuan as models_harga

def create_pembelian(db: Session, tipe_sampah: int, berat: float, nasabah_id: int):

    # 1. Add to sampah
    sampah = models_sampah.Sampah(tipe_sampah=tipe_sampah, berat=berat)
    db.add(sampah)
    db.flush()  # To get sampah.id before commit

    # 2. Calculate harga beli
    harga = db.query(models_harga.HargaSatuan).filter_by(tipe_sampah=tipe_sampah).first()
    if not harga:
        raise ValueError("Harga sampah tidak ditemukan")

    harga_beli = harga.satuan_beli * berat

    # 3. Add to pembelian
    pembelian = models_pembelian.Pembelian(
        nasabah_id=nasabah_id,
        sampah_id=sampah.sampah_id,
        harga_beli=harga_beli
    )
    db.add(pembelian)
    db.commit()

    # Will refresh the pembelian table
    db.refresh(pembelian)

    return pembelian