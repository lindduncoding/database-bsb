from fastapi import FastAPI
from api import beli, jual

app = FastAPI()

app.include_router(beli.router, prefix="/beli", tags=["Beli"])
app.include_router(jual.router, prefix="/jual", tags=["Jual"])
# app.include_router(harga.router, prefix="/harga-satuan", tags=["Harga Satuan"])

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)