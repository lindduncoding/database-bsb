from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from models import Pembelian, Penjualan, Sampah
from config import get_db
from fastapi.templating import Jinja2Templates

from crud.export import export_table_as_dataframe
from crud.sampah import lihat_sampah

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("layout.html", {
        "request": request
    })

@router.get("/pembelian", response_class=HTMLResponse)
def pembelian_dashboard(request: Request, db: Session = Depends(get_db)):
    df = export_table_as_dataframe(db, Pembelian)
    return templates.TemplateResponse("pembelian.html", {
        "request": request,
        "items": df.to_dict(orient="records")
    })

@router.get("/penjualan", response_class=HTMLResponse)
def penjualan_dashboard(request: Request, db: Session = Depends(get_db)):
    df = export_table_as_dataframe(db, Penjualan)
    return templates.TemplateResponse("penjualan.html", {
        "request": request,
        "items": df.to_dict(orient="records")
    })

@router.get("/sampah", response_class=HTMLResponse)
def sampah_dashboard(request: Request, db: Session = Depends(get_db)):
    items = lihat_sampah(db)
    return templates.TemplateResponse("sampah.html", {
        "request": request,
        "items": items
    })