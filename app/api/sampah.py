from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Optional

# User defined imports
from config import get_db
from crud import sampah as crud_sampah

router = APIRouter()

# Pydantic is for data validation, unlike Mongoose that automatically validates data

class LihatSampahRequest(BaseModel):
    sold: Optional[bool] = None
    tipe_sampah: Optional[bool] = None

class SampahOut(BaseModel):
    sampah_id: int
    tipe_sampah: int
    stok: float

# Already defined in main to have prefix "beli"
@router.get("/", response_model=List[SampahOut])
def lihat(request: Optional[LihatSampahRequest], db: Session = Depends(get_db)):
    try:
        sampah = crud_sampah.lihat_sampah(
            db=db,
            tipe_sampah=request.tipe_sampah if request else None,
            sold=request.sold if request else None
        )

        return sampah

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))
