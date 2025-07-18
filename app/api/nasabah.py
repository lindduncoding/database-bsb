from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

# User defined imports
from config import get_db
from crud import nasabah as crud_nasabah

router = APIRouter()

# Pydantic is for data validation, unlike Mongoose that automatically validates data

class NasabahRequest(BaseModel):
    nama: str

# Already defined in main to have prefix "nasabah"
@router.post("/")
def nasabah(request: NasabahRequest, db: Session = Depends(get_db)):
    try:
        nasabah = crud_nasabah.make_nasabah(
            db=db,
            nama=request.nama
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
