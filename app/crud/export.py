from sqlalchemy.orm import Session
import pandas as pd
from typing import Type
from sqlalchemy.ext.declarative import DeclarativeMeta

def export_table_as_dataframe(
    db: Session, 
    model: Type[DeclarativeMeta]
    ) -> pd.DataFrame:
    data = db.query(model).all()
    
    if not data:
        return pd.DataFrame()

    # Extract column names from SQLAlchemy model
    columns = [column.name for column in model.__table__.columns]

    # Build dataframe
    df = pd.DataFrame([{col: getattr(row, col) for col in columns} for row in data])
    return df
