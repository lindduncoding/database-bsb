from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

# User defined imports
from config import get_db
from crud import jual as crud_jual

router = APIRouter()

# Pydantic is for data validation, unlike Mongoose that automatically validates data

class JualRequest(BaseModel):
    sampah_id: int
    berat: float
    pembeli_id: int

# Already defined in main to have prefix "jual"
@router.post("/")
def jual(request: JualRequest, db: Session = Depends(get_db)):
    try:
        pemjualan = crud_jual.create_penjualan(
            db=db,
            sampah_id=request.sampah_id,
            berat=request.berat,
            pembeli_id=request.pembeli_id
        )
        return {
            "message": "Pemjualan berhasil",
            "invoice_no": pemjualan.no_invoice,
            "harga_jual": pemjualan.harga_jual
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))
