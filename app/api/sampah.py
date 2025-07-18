from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from config import get_db
from crud import sampah as crud_sampah

router = APIRouter()

class SampahOut(BaseModel):
    sampah_id: int
    tipe_sampah: int
    stok: float
    is_sold: bool

    class Config:
        from_atrributes = True

@router.get("/", response_model=List[SampahOut])
def lihat_sampah(
    sold: Optional[bool] = Query(None),
    tipe_sampah: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    try:
        return crud_sampah.lihat_sampah(
            db=db,
            sold=sold,
            tipe_sampah=tipe_sampah
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
