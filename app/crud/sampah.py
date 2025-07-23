from sqlalchemy.orm import Session
from typing import Optional, List, Dict
from models import sampah as models_sampah, harga_satuan as models_harga

def lihat_sampah(
    db: Session,
    sold: Optional[bool] = None,
    tipe_sampah: Optional[int] = None
) -> List[Dict]:
    query = db.query(
        models_sampah.Sampah,
        models_harga.HargaSatuan.nama_sampah
    ).join(
        models_harga.HargaSatuan,
        models_sampah.Sampah.tipe_sampah == models_harga.HargaSatuan.tipe_sampah
    )

    if sold is not None:
        query = query.filter(models_sampah.Sampah.is_sold == sold)

    if tipe_sampah is not None:
        query = query.filter(models_sampah.Sampah.tipe_sampah == tipe_sampah)

    results = query.all()

    return [
        {
            "sampah_id": sampah.sampah_id,
            "stok": sampah.stok,
            "is_sold": sampah.is_sold,
            "tipe_sampah": sampah.tipe_sampah,
            "nama_sampah": nama_sampah
        }
        for sampah, nama_sampah in results
    ]

