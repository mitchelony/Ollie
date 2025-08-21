from pydantic import BaseModel, Field, field_validator
from pydantic import ConfigDict
from datetime import date
from typing import Optional

class ExpenseValidatorsMixin(BaseModel):
    @field_validator("amount", check_fields=False)
    @classmethod
    def validate_amount_non_negative(cls, v: float):
        if v < 0:
            raise ValueError("amount must be >= 0")
        return v

    @field_validator("date", check_fields=False)
    @classmethod
    def validate_date_not_in_future(cls, v: Optional[date]):
        if v is None:
            return v
        if v > date.today():
            raise ValueError("date cannot be in the future")
        return v

class ExpenseBase(ExpenseValidatorsMixin):
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

class ExpensePut(ExpenseValidatorsMixin):
    """Schema for full replacement via PUT (all keys required)."""
    amount: float
    category: str
    date: date
    # Require presence of nullable fields; allow None
    description: Optional[str] = Field(...)
    payment_method: Optional[str] = Field(...)
    merchant: Optional[str] = Field(...)
    is_recurring: bool = Field(...)

class ExpensePatch(ExpenseValidatorsMixin):
    """Schema for partial update via PATCH (all optional)."""
    amount: Optional[float] = None
    category: Optional[str] = None
    date: Optional["date"] = None
    description: Optional[str] = None
    payment_method: Optional[str] = None
    merchant: Optional[str] = None
    is_recurring: Optional[bool] = None

class ExpenseOut(ExpenseBase):
    """Schema for reading expenses, includes the database-generated ID."""
    id: int

    model_config = ConfigDict(from_attributes=True)
