from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from models import Pembelian, Penjualan, Sampah, HargaSatuan, Nasabah, Pembeli
from config import get_db
from fastapi.templating import Jinja2Templates
from typing import Annotated

from crud.export import export_table_as_dataframe
from crud.sampah import lihat_sampah
from crud.nasabah import get_all_nasabah
from crud.harga import get_harga

router = APIRouter()
templates = Jinja2Templates(directory="templates")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("login.html", {
        "request": request
    })

@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(token: Annotated[str, Depends(oauth2_scheme)], request: Request):
    return templates.TemplateResponse("layout.html", {
        "request": request
    })

@router.get("/pembelian", response_class=HTMLResponse)
def pembelian_dashboard(token: Annotated[str, Depends(oauth2_scheme)], request: Request, db: Session = Depends(get_db)):
    df = export_table_as_dataframe(db, Pembelian)
    return templates.TemplateResponse("pembelian.html", {
        "request": request,
        "items": df.to_dict(orient="records")
    })

@router.get("/penjualan", response_class=HTMLResponse)
def penjualan_dashboard(token: Annotated[str, Depends(oauth2_scheme)], request: Request, db: Session = Depends(get_db)):
    df = export_table_as_dataframe(db, Penjualan)
    return templates.TemplateResponse("penjualan.html", {
        "request": request,
        "items": df.to_dict(orient="records")
    })

@router.get("/sampah", response_class=HTMLResponse)
def sampah_dashboard(token: Annotated[str, Depends(oauth2_scheme)], request: Request, db: Session = Depends(get_db)):
    items = lihat_sampah(db)
    return templates.TemplateResponse("sampah.html", {
        "request": request,
        "items": items
    })

@router.get("/beli", response_class=HTMLResponse)
async def get_pembelian_form(token: Annotated[str, Depends(oauth2_scheme)], request: Request, db: Session = Depends(get_db)):
    harga_satuan = db.query(HargaSatuan).all()
    return templates.TemplateResponse("beli.html", {
        "request": request,
        "harga_satuan": harga_satuan
    })

@router.get("/jual", response_class=HTMLResponse)
async def get_penjualan_form(token: Annotated[str, Depends(oauth2_scheme)], request: Request, db: Session = Depends(get_db)):
    harga_satuan = db.query(HargaSatuan).all()
    return templates.TemplateResponse("jual.html", {
        "request": request,
        "harga_satuan": harga_satuan
    })

@router.get("/nasabah", response_class=HTMLResponse)
def nasabah_dashboard(token: Annotated[str, Depends(oauth2_scheme)], request: Request, db: Session = Depends(get_db)):
    items = get_all_nasabah(db)
    return templates.TemplateResponse("nasabah.html", {
        "request": request,
        "items": items
    })

@router.get("/harga", response_class=HTMLResponse)
def harga_dashboard(token: Annotated[str, Depends(oauth2_scheme)], request: Request, db: Session = Depends(get_db)):
    items = get_harga(db)
    return templates.TemplateResponse("upload_harga.html", {
        "request": request,
        "items": items
    })