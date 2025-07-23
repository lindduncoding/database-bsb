from sqlalchemy.orm import Session
import pandas as pd
from typing import Type
from sqlalchemy.ext.declarative import DeclarativeMeta
from models import nasabah as models_nasabah, harga_satuan as models_harga, sampah as models_sampah, pembeli as models_pembeli

def export_table_as_dataframe(
    db: Session, 
    model: Type[DeclarativeMeta]
) -> pd.DataFrame:
    if model.__tablename__ == "pembelian":
        data = (
            db.query(
                model,
                models_nasabah.Nasabah.no_rekening,
                models_harga.HargaSatuan.nama_sampah
            )
            .join(models_nasabah.Nasabah, model.nasabah_id == models_nasabah.Nasabah.nasabah_id)
            .join(models_sampah.Sampah, model.sampah_id == models_sampah.Sampah.sampah_id)
            .join(models_harga.HargaSatuan, models_sampah.Sampah.tipe_sampah == models_harga.HargaSatuan.tipe_sampah)
            .all()
        )

        columns = [column.name for column in model.__table__.columns]
        df = pd.DataFrame([
            {
                **{col: getattr(pembelian, col) for col in columns},
                "no_rekening": no_rekening,
                "nama_sampah": nama_sampah
            }
            for pembelian, no_rekening, nama_sampah in data
        ])
        df.drop(columns=["nasabah_id", "sampah_id"], inplace=True)

    elif model.__tablename__ == "penjualan":
        data = (
            db.query(
                model,
                models_pembeli.Pembeli.no_pembeli,
                models_harga.HargaSatuan.nama_sampah
            )
            .join(models_pembeli.Pembeli, model.pembeli_id == models_pembeli.Pembeli.pembeli_id)
            .join(models_sampah.Sampah, model.sampah_id == models_sampah.Sampah.sampah_id)
            .join(models_harga.HargaSatuan, models_sampah.Sampah.tipe_sampah == models_harga.HargaSatuan.tipe_sampah)
            .all()
        )

        columns = [column.name for column in model.__table__.columns]
        df = pd.DataFrame([
            {
                **{col: getattr(penjualan, col) for col in columns},
                "no_pembeli": no_pembeli,
                "nama_sampah": nama_sampah
            }
            for penjualan, no_pembeli, nama_sampah in data
        ])
        df.drop(columns=["pembeli_id", "sampah_id"], inplace=True)

    else:
        data = db.query(model).all()
        if not data:
            return pd.DataFrame()

        columns = [column.name for column in model.__table__.columns]
        df = pd.DataFrame([{col: getattr(row, col) for col in columns} for row in data])

    return df

