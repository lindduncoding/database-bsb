from sqlalchemy.orm import Session
from typing import List, Dict
from models.harga_satuan import HargaSatuan
import pandas as pd

def upload_harga(db: Session, df: pd.DataFrame):
    required_columns = {"nama_sampah", "satuan_beli", "satuan_jual"}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"Kolom tidak sesuai: {required_columns}")

    # Upsert by nama_sampah
    for _, row in df.iterrows():
        nama_sampah = row["nama_sampah"].strip()
        satuan_beli = float(row["satuan_beli"])
        satuan_jual = float(row["satuan_jual"])

        harga = db.query(HargaSatuan).filter_by(nama_sampah=nama_sampah).first()
        if harga:
            harga.satuan_beli = satuan_beli
            harga.satuan_jual = satuan_jual
        else:
            new_harga = HargaSatuan(
                nama_sampah=nama_sampah,
                satuan_beli=satuan_beli,
                satuan_jual=satuan_jual
            )
            db.add(new_harga)

    db.commit()

def get_harga(db:Session)->List[Dict]:
    harga = db.query(HargaSatuan).all()
    return harga