from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Table
from app.schemas import TableCreate, TableUpdate
from app.utils import admin_required

router = APIRouter()

@router.get("/tables", dependencies=[Depends(admin_required)])
def get_all_tables(db: Session = Depends(get_db)):
    tables = db.query(Table).all()
    return tables

@router.post("/tables", dependencies=[Depends(admin_required)])
def add_table(table: TableCreate, db: Session = Depends(get_db)):
    new_table = Table(**table.dict())
    db.add(new_table)
    db.commit()
    db.refresh(new_table)
    return {"message": "Table added successfully", "table": new_table}

@router.put("/tables/{table_id}", dependencies=[Depends(admin_required)])
def update_table(table_id: int, table: TableUpdate, db: Session = Depends(get_db)):
    table_data = db.query(Table).filter(Table.id == table_id).first()
    if not table_data:
        raise HTTPException(status_code=404, detail="Table not found")
    for key, value in table.dict(exclude_unset=True).items():
        setattr(table_data, key, value)
    db.commit()
    return {"message": "Table updated successfully", "table": table_data}

@router.delete("/tables/{table_id}", dependencies=[Depends(admin_required)])
def delete_table(table_id: int, db: Session = Depends(get_db)):
    table_data = db.query(Table).filter(Table.id == table_id).first()
    if not table_data:
        raise HTTPException(status_code=404, detail="Table not found")
    db.delete(table_data)
    db.commit()
    return {"message": "Table deleted successfully"}
