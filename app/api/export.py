from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import io
import pandas as pd
from typing import Annotated

from config import get_db
from crud.export import export_table_as_dataframe
from models.pembelian import Pembelian
from models.penjualan import Penjualan

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/export/{table_name}")
def export_data(
    token: Annotated[str, Depends(oauth2_scheme)],
    table_name: str,
    format: str = Query("csv", enum=["csv", "xlsx"]),
    db: Session = Depends(get_db)
):
    model_map = {
        "pembelian": Pembelian,
        "penjualan": Penjualan
    }

    model = model_map.get(table_name.lower())
    if not model:
        raise HTTPException(status_code=404, detail="Invalid table name")

    df = export_table_as_dataframe(db, model)

    if df.empty:
        raise HTTPException(status_code=404, detail="No data found")

    if format == "csv":
        return StreamingResponse(
            io.StringIO(df.to_csv(index=False)),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={table_name}.csv"}
        )
    elif format == "xlsx":
        output = io.BytesIO()
        df.to_excel(output, index=False)
        output.seek(0)
        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={table_name}.xlsx"}
        )
