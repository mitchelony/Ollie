from pydantic import BaseModel
from datetime import date
from typing import Optional

class ExpenseBase(BaseModel):
    amount: float
    category: str
    date: date
    description: Optional[str] = None
    payment_method: Optional[str] = None
    merchant: Optional[str] = None
    is_recurring: Optional[bool] = False

class ExpenseCreate(ExpenseBase):
    """Schema for creating new expenses. Inherits all fields from ExpenseBase."""
    pass

class ExpenseOut(ExpenseBase):
    """Schema for reading expenses, includes the database-generated ID."""
    id: int

    class Config:
        orm_mode = True
