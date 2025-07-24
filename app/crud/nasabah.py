from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict
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

def get_nasabah_profit(no_rekening: str, db: Session)->List[Dict]:
    nasabah = db.query(models_nasabah.Nasabah).filter_by(no_rekening=no_rekening).first()
    nasabah_id = nasabah.nasabah_id
    total_beli = db.query(func.sum(models_pembelian.Pembelian.harga_beli)).filter_by(nasabah_id=nasabah_id).scalar() or 0
    return {"no_rekening": no_rekening, "tabungan": total_beli}

def get_all_nasabah(db: Session)->List[Dict]:
    nasabah = db.query(models_nasabah.Nasabah).all()
    return nasabah
