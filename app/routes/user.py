from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Table
from app.utils import user_required

router = APIRouter()

@router.get("/tables", dependencies=[Depends(user_required)])
def view_available_tables(db: Session = Depends(get_db)):
    tables = db.query(Table).filter_by(is_reserved=False).all()
    return tables

@router.post("/tables/reserve", dependencies=[Depends(user_required)])
def reserve_table(table_id: int, db: Session = Depends(get_db)):
    table = db.query(Table).filter(Table.id == table_id, Table.is_reserved == False).first()
    if not table:
        raise HTTPException(status_code=404, detail="Table not available for reservation")
    table.is_reserved = True
    db.commit()
    return {"message": "Table reserved successfully", "table": table}

@router.delete("/tables/cancel", dependencies=[Depends(user_required)])
def cancel_reservation(table_id: int, db: Session = Depends(get_db)):
    table = db.query(Table).filter(Table.id == table_id, Table.is_reserved == True).first()
    if not table:
        raise HTTPException(status_code=404, detail="Reservation not found")
    table.is_reserved = False
    db.commit()
    return {"message": "Reservation canceled successfully"}
