from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from pydantic import BaseModel
from sqlalchemy.orm import Session

# User defined imports
from config import get_db
from crud import nasabah as crud_nasabah

router = APIRouter()

# Pydantic is for data validation, unlike Mongoose that automatically validates data

class NasabahRequest(BaseModel):
    nama: str
    dusun: str
    desa: str
    kecamatan: str
    kota_kabupaten: str
    provinsi: str
    kode_pos: str

class NasabahResponse(BaseModel):
    nama: str
    no_rekening: str
    dusun: str
    desa: str
    kecamatan: str
    kota_kabupaten: str
    provinsi: str
    kode_pos: str

    class Config:
        from_atrributes = True

class ProfitResponse(BaseModel):
    no_rekening: str
    tabungan: float

    class Config:
        from_atrributes = True

# Already defined in main to have prefix "nasabah"
@router.post("/daftar")
def nasabah(request: NasabahRequest, db: Session = Depends(get_db)):
    try:
        nasabah = crud_nasabah.make_nasabah(
            db=db,
            nama=request.nama,
            dusun=request.dusun,
            desa=request.desa,
            kecamatan=request.kecamatan,
            kota_kabupaten=request.kota_kabupaten,
            provinsi=request.provinsi,
            kode_pos=request.kode_pos
        )
        return {
            "message": "Pendaftaran berhasil!",
            "nama": nasabah.nama,
            "no_rekening": nasabah.no_rekening
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/")
def list_nasabah(db: Session = Depends(get_db), response_model=List[NasabahResponse]):
    try:
        return crud_nasabah.get_all_nasabah(db=db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/profit")
def list_profit(no_rekening: str=Query(), db: Session = Depends(get_db), response_model=List[ProfitResponse]):
    try:
        return crud_nasabah.get_nasabah_profit(db=db, no_rekening=no_rekening)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))