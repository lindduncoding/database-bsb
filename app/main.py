from fastapi import FastAPI
from api import beli, jual, harga, sampah, nasabah, export
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
app = FastAPI()

app.include_router(beli.router, prefix="/beli", tags=["Beli"])
app.include_router(jual.router, prefix="/jual", tags=["Jual"])
app.include_router(harga.router, prefix="/harga", tags=["Harga Satuan"])
app.include_router(sampah.router, prefix="/sampah", tags=["Sampah"])
app.include_router(nasabah.router, prefix="/nasabah", tags=["Nasabah"])
app.include_router(export.router, tags=["Export"])

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)