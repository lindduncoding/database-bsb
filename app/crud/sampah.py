from sqlalchemy.orm import Session
from typing import Optional, List
from models import sampah as models_sampah

def lihat_sampah(
    db: Session,
    sold: Optional[bool] = None,
    tipe_sampah: Optional[int] = None
) -> List[models_sampah.Sampah]:
    query = db.query(models_sampah.Sampah)

    if sold is not None:
        query = query.filter(models_sampah.Sampah.is_sold == sold)

    if tipe_sampah is not None:
        query = query.filter(models_sampah.Sampah.tipe_sampah == tipe_sampah)

    return query.all()
