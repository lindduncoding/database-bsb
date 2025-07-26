from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Annotated
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer

from config import get_db
from crud import sampah as crud_sampah

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class SampahOut(BaseModel):
    sampah_id: int
    tipe_sampah: int
    stok: float
    is_sold: bool
    nama_sampah: str

    class Config:
        from_atrributes = True

@router.get("/", response_model=List[SampahOut])
def lihat_sampah(
    token: Annotated[str, Depends(oauth2_scheme)],
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
