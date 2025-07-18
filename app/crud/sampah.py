from sqlalchemy.orm import Session
from models import sampah as models_sampah

def lihat_sampah(db: Session, sold: bool, tipe_sampah:int ):
    
    # Returns only sold or unsold garbage
    if sold is not None:
        sampah = db.query(models_sampah.Sampah).filter(models_sampah.Sampah.is_sold == is_sold)
    if tipe_sampah is not None:
        sampah = db.query(models_sampah.Sampah).filter(models_sampah.Sampah.tipe_sampah == tipe_sampah)

    sampah = db.query(models_sampah.Sampah).all()

    return sampah