from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Annotated

# User defined imports
from config import get_db
from crud import beli as crud_beli

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Pydantic is for data validation, unlike Mongoose that automatically validates data

class BeliRequest(BaseModel):
    tipe_sampah: int
    berat: float
    no_rekening: str

# Already defined in main to have prefix "beli"
@router.post("/")
def beli(token: Annotated[str, Depends(oauth2_scheme)], request: BeliRequest, db: Session = Depends(get_db)):
    try:
        pembelian = crud_beli.create_pembelian(
            db=db,
            tipe_sampah=request.tipe_sampah,
            berat=request.berat,
            no_rekening=request.no_rekening
        )
        return {
            "message": "Pembelian berhasil",
            "invoice_no": pembelian.no_invoice,
            "harga_beli": pembelian.harga_beli
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))
