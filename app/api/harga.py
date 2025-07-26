from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from pydantic import BaseModel
import pandas as pd
from io import StringIO
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer

from config import get_db
from crud import harga as crud_harga

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class HargaResponse(BaseModel):
    tipe_sampah: int
    nama_sampah: str
    satuan_beli: float
    satuan_jual: float

    class Config:
        from_atrributes = True

@router.post("/upload-csv/")
async def upload_harga_csv(token: Annotated[str, Depends(oauth2_scheme)], file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a CSV")

    try:
        contents = await file.read()
        df = pd.read_csv(StringIO(contents.decode("utf-8")))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse CSV: {e}")

    try:
        crud_harga.upload_harga(db, df)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

    return {"message": "CSV processed and database updated successfully"}

@router.get("/", response_model=List[HargaResponse])
def lihat_harga(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    try:
        return crud_harga.get_harga(db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
