from sqlalchemy.orm import Session
from models import nasabah as models_nasabah, pembelian as models_pembelian

def make_nasabah(nama: str, db: Session):
    nasabah = models_nasabah.Nasabah(nama=nama)
    db.add(nasabah)
    db.flush()
    db.commit()
    db.refresh(nasabah) 
    return nasabah

def get_nasabah_profit(nasabah_id: int, db: Session):
    total_beli = db.query(func.sum(models_pembelian.Pembelian.harga_beli)).filter_by(nasabah_id=nasabah_id).scalar() or 0
    return {"nasabah_id": nasabah_id, "tabungan": total_beli}
