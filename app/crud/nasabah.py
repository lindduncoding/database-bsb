from sqlalchemy.orm import Session
from models import nasabah as models_nasabah, pembelian as models_pembelian

def make_nasabah(
    nama: str, 
    dusun: str, desa: str, kecamatan: str, 
    kota_kabupaten: str, provinsi: str, 
    kode_pos: str, 
    db: Session):
    nasabah = models_nasabah.Nasabah(nama=nama, dusun=dusun, desa=desa, kecamatan=kecamatan, kota_kabupaten=kota_kabupaten, provinsi=provinsi, kode_pos=kode_pos)
    db.add(nasabah)
    db.flush()
    db.commit()
    db.refresh(nasabah) 
    return nasabah

def get_nasabah_profit(nasabah_id: int, db: Session):
    total_beli = db.query(func.sum(models_pembelian.Pembelian.harga_beli)).filter_by(nasabah_id=nasabah_id).scalar() or 0
    return {"nasabah_id": nasabah_id, "tabungan": total_beli}
