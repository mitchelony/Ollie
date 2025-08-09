# Imports
from fastapi import APIRouter, Depends, HTTPException, Query, Response, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from sqlalchemy import or_, func
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import logging

from app.models.expense import Expense
from app.schemas.expense import ExpenseCreate, ExpenseOut, ExpensePut, ExpensePatch
from app.db import get_db

logger = logging.getLogger(__name__)

# Router instance
router = APIRouter(prefix="/expenses", tags=["Expenses"])

# Helper: build query with filters
def _build_expenses_query(
    db_session: Session,
    *,
    category: Optional[str] = None,
    categories: Optional[List[str]] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    is_recurring: Optional[bool] = None,
    merchant: Optional[str] = None,
    merchant_like: Optional[str] = None,
    payment_method: Optional[str] = None,
    q: Optional[str] = None,
    since_id: Optional[int] = None,
    max_id: Optional[int] = None,
):
    query = db_session.query(Expense)

    # Amount filters
    if min_amount is not None:
        query = query.filter(Expense.amount >= min_amount)
    if max_amount is not None:
        query = query.filter(Expense.amount <= max_amount)

    # Category filters (case-insensitive, supports single or multiple)
    cats: List[str] = []
    if category:
        cats.append(category)
    if categories:
        cats.extend(categories)
    if cats:
        lowered = [c.lower() for c in cats]
        query = query.filter(func.lower(Expense.category).in_(lowered))

    # Date filters
    if start_date is not None:
        query = query.filter(Expense.date >= start_date)
    if end_date is not None:
        query = query.filter(Expense.date <= end_date)

    # Boolean
    if is_recurring is not None:
        query = query.filter(Expense.is_recurring == is_recurring)

    # Merchant / Payment method
    if merchant is not None:
        query = query.filter(func.lower(Expense.merchant) == merchant.lower())
    if merchant_like is not None:
        like_term = f"%{merchant_like}%"
        query = query.filter(Expense.merchant.ilike(like_term))
    if payment_method is not None:
        query = query.filter(func.lower(Expense.payment_method) == payment_method.lower())

    # Text search
    if q:
        like = f"%{q}%"
        query = query.filter(
            or_(
                Expense.description.ilike(like),
                Expense.merchant.ilike(like),
                Expense.category.ilike(like),
                Expense.payment_method.ilike(like),
            )
        )

    # ID cursors
    if since_id is not None:
        query = query.filter(Expense.id > since_id)
    if max_id is not None:
        query = query.filter(Expense.id <= max_id)

    return query

# POST Route
@router.post("/", response_model=ExpenseOut, status_code=201)
def create_expense(
    expense_data: ExpenseCreate,
    response: Response,
    db_session: Session = Depends(get_db),
):
    new_expense = Expense(**expense_data.model_dump())
    db_session.add(new_expense)
    try:
        db_session.commit()
        db_session.refresh(new_expense)
        # Location header for the created resource
        response.headers["Location"] = f"/expenses/{new_expense.id}"
    except IntegrityError:
        db_session.rollback()
        logger.exception("Integrity error while creating expense")
        raise HTTPException(status_code=409, detail="Conflict creating expense")
    except SQLAlchemyError:
        db_session.rollback()
        logger.exception("Database error while creating expense")
        raise HTTPException(status_code=500, detail="Database error")

    return new_expense

# GET Route
@router.get("/", response_model=List[ExpenseOut])
def get_all_expenses(
    category: Optional[str] = None,
    categories: Optional[List[str]] = Query(None, description="Repeat param to filter by multiple categories"),
    min_amount: Optional[float] = Query(None, ge=0),
    max_amount: Optional[float] = Query(None, ge=0),
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    is_recurring: Optional[bool] = None,
    merchant: Optional[str] = None,
    merchant_like: Optional[str] = None,
    payment_method: Optional[str] = None,
    q: Optional[str] = Query(None, description="Search in description, merchant, category, payment method"),
    since_id: Optional[int] = Query(None, ge=0),
    max_id: Optional[int] = Query(None, ge=0),
    sort_by: str = Query("date", description="One of: id, date, amount, category, merchant"),
    sort_dir: str = Query("desc", description="asc or desc"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db_session: Session = Depends(get_db),
    response: Optional[Response] = None,
):
    # Validate ranges
    if min_amount is not None and max_amount is not None and min_amount > max_amount:
        raise HTTPException(status_code=400, detail="min_amount cannot be greater than max_amount")
    if start_date is not None and end_date is not None and start_date > end_date:
        raise HTTPException(status_code=400, detail="start_date cannot be after end_date")

    # Build base query via helper
    query = _build_expenses_query(
        db_session,
        category=category,
        categories=categories,
        min_amount=min_amount,
        max_amount=max_amount,
        start_date=start_date,
        end_date=end_date,
        is_recurring=is_recurring,
        merchant=merchant,
        merchant_like=merchant_like,
        payment_method=payment_method,
        q=q,
        since_id=since_id,
        max_id=max_id,
    )

    # Total count before pagination
    total = query.count()
    if response is not None:
        response.headers["X-Total-Count"] = str(total)

    # Sorting with stable tie-breaker by id
    sortable = {
        "id": Expense.id,
        "date": Expense.date,
        "amount": Expense.amount,
        "category": Expense.category,
        "merchant": Expense.merchant,
    }
    sort_col = sortable.get(sort_by)
    if sort_col is None:
        allowed = ", ".join(sorted(sortable.keys()))
        raise HTTPException(status_code=400, detail=f"Invalid sort_by. Allowed: {allowed}")
    if sort_dir not in ("asc", "desc"):
        raise HTTPException(status_code=400, detail="Invalid sort_dir. Use 'asc' or 'desc'")
    primary_order = sort_col.desc() if sort_dir == "desc" else sort_col.asc()
    tie_break = Expense.id.desc() if sort_dir == "desc" else Expense.id.asc()
    query = query.order_by(primary_order, tie_break)

    # Pagination
    expenses = query.offset(offset).limit(limit).all()
    return expenses

# GET Route by ID
@router.get("/{expense_id}", response_model=ExpenseOut)
def get_expense_by_id(
    expense_id: int = Path(..., gt=0),
    db_session: Session = Depends(get_db),
):
    expense = db_session.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense

# PUT Route (full update)
@router.put("/{expense_id}", response_model=ExpenseOut)
def update_expense(
    updated_data: ExpensePut,
    expense_id: int = Path(..., gt=0),
    db_session: Session = Depends(get_db),
):
    expense = db_session.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    # Replace all fields
    data = updated_data.model_dump()
    for field, value in data.items():
        setattr(expense, field, value)

    try:
        db_session.commit()
        db_session.refresh(expense)
    except IntegrityError:
        db_session.rollback()
        logger.exception("Integrity error while updating expense")
        raise HTTPException(status_code=409, detail="Conflict updating expense")
    except SQLAlchemyError:
        db_session.rollback()
        logger.exception("Database error while updating expense")
        raise HTTPException(status_code=500, detail="Database error")

    return expense

# PATCH Route (partial update)
@router.patch("/{expense_id}", response_model=ExpenseOut)
def patch_expense(
    updates: ExpensePatch,
    expense_id: int = Path(..., gt=0),
    db_session: Session = Depends(get_db),
):
    expense = db_session.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(expense, field, value)

    try:
        db_session.commit()
        db_session.refresh(expense)
    except IntegrityError:
        db_session.rollback()
        logger.exception("Integrity error while patching expense")
        raise HTTPException(status_code=409, detail="Conflict patching expense")
    except SQLAlchemyError:
        db_session.rollback()
        logger.exception("Database error while patching expense")
        raise HTTPException(status_code=500, detail="Database error")

    return expense

# DELETE Route
@router.delete("/{expense_id}", status_code=204)
def delete_expense(
    expense_id: int = Path(..., gt=0),
    db_session: Session = Depends(get_db),
):
    expense = db_session.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    # Snapshot for audit log before deletion
    date_value = getattr(expense, "date", None)
    deleted_info = {
        "id": expense.id,
        "amount": expense.amount,
        "category": expense.category,
        "date": date_value.isoformat() if isinstance(date_value, date) else None,
        "merchant": expense.merchant,
        "payment_method": expense.payment_method,
        "is_recurring": expense.is_recurring,
    }

    db_session.delete(expense)
    try:
        db_session.commit()
        logger.info("Deleted expense: %s", deleted_info)
    except SQLAlchemyError:
        db_session.rollback()
        logger.exception("Database error while deleting expense")
        raise HTTPException(status_code=500, detail="Database error")

    return Response(status_code=204)