from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
from io import StringIO

from config import get_db
from crud import harga as crud_harga

router = APIRouter()

@router.post("/upload-csv/")
async def upload_harga_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
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
