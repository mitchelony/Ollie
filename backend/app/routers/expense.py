# Imports
import re
from urllib import response
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models.expense import Expense
from app.schemas.expense import ExpenseCreate, ExpenseOut
from app.db import SessionLocal, get_db
from app.models import expense

# Router instance
router = APIRouter(prefix="/expenses", tags=["Expenses"])

# Test Route
# @router.get("/")
# def health_check():
#     return {"message": "Expense Route Active"}

# POST Route
@router.post ("/", response_model=ExpenseOut)
def create_expense(
    expense_data: ExpenseCreate, db_session: Session = Depends(get_db)
):
    new_expense = Expense(**expense_data.dict())
    db_session.add(new_expense)
    db_session.commit()
    db_session.refresh(new_expense)

    return new_expense

# GET Route
@router.get("/", response_model=List[ExpenseOut])
def get_all_expenses(
    db_session: Session = Depends(get_db)
):
    expenses = db_session.query(Expense). all()
    if not expenses:
        raise HTTPException(status_code=404, detail="No expenses found")
    return expenses

# GET Route by ID
# @router.get("/{expense_id}", response_model=ExpenseOut)
# def get_expense_by_id(
#     expense_id: int, db_session: Session = Depends(get_db)
# ):
#     expense = db_session.query(Expense).filter(Expense.id == expense_id).first()
#     if not expense:
#         raise HTTPException(status_code=404, detail="Expense not found")
#     return expense

# PUT Route
@router.put("/{expense_id}", response_model=ExpenseOut)
def update_expenses(
    expense_id: int,
    updated_data: ExpenseCreate,
    db_session: Session = Depends(get_db)
):
    expense = db_session.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    for field, value in updated_data.dict().items():
        setattr(expense, field, value)
    db_session.commit()
    db_session.refresh(expense)
    return expense

@router.delete("/{expense_id}")
def delete_expense(
    expense_id: int, db_session: Session = Depends((get_db))
):
    expense = db_session.query(Expense).filter(Expense.id == expense_id).first()
    
    if not expense:
        raise HTTPException(status_code = 404, detail = "Expense Not Found")
    
    db_session.delete(expense)
    db_session.commit()