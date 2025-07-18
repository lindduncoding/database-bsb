from sqlalchemy.orm import Session
from models import sampah as models_sampah, penjualan as models_penjualan, harga_satuan as models_harga, pembeli as models_pembeli

def create_penjualan(db: Session, tipe_sampah: int, berat: float, nama_pembeli: str):

    # 1. Select tipe_sampah
    sampah = db.query(models_sampah.Sampah).filter_by(tipe_sampah=tipe_sampah).first()
    if not sampah:
        raise ValueError("Sampah tidak ditemukan")
    if sampah.stok < berat:
        raise ValueError("Stok sampah tidak mencukupi!")
    else:
        sampah.stok -= berat
    if sampah.is_sold:
        raise ValueError("Sampah sudah terjual")

    tipe_sampah = sampah.tipe_sampah

    # 2. Calculate harga jual
    harga = db.query(models_harga.HargaSatuan).filter_by(tipe_sampah=tipe_sampah).first()
    if not harga:
        raise ValueError("Harga sampah tidak ditemukan")

    harga_jual = harga.satuan_jual * berat

    # 3. Add to penjualan
    # 3.5 Golek pembeli_id sek
    pembeli = db.query(models_pembeli.Pembeli).filter_by(nama=nama_pembeli).first()

    if pembeli:
        pembeli_id = pembeli.pembeli_id
    else:
        new_pembeli = models_pembeli.Pembeli(nama=nama_pembeli)
        db.add(new_pembeli)
        db.flush()
        pembeli_id = new_pembeli.pembeli_id

    penjualan = models_penjualan.Penjualan(
        pembeli_id=pembeli_id,
        sampah_id=sampah.sampah_id,
        berat=berat,
        harga_jual=harga_jual
    )
    db.add(penjualan)

    # 4. Set to sold
    if sampah.stok == 0:
        sampah.is_sold = True
    
    # Will refresh the penjualan table
    db.commit()
    db.refresh(penjualan)

    return penjualan