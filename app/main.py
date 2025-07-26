from fastapi import FastAPI
from api import beli, jual, harga, sampah, nasabah, export, frontend, auth
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Backend routers
app.include_router(beli.router, prefix="/api/beli", tags=["Beli"])
app.include_router(jual.router, prefix="/api/jual", tags=["Jual"])
app.include_router(harga.router, prefix="/api/harga", tags=["Harga Satuan"])
app.include_router(sampah.router, prefix="/api/sampah", tags=["Sampah"])
app.include_router(nasabah.router, prefix="/api/nasabah", tags=["Nasabah"])
app.include_router(export.router, prefix="/api", tags=["Export"])
app.include_router(auth.router, tags=["Auth"])

# Frontend router
app.include_router(frontend.router, tags=["frontend"])

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)