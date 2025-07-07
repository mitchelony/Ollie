from sqlalchemy import Column, Integer, String, Float, Boolean, Date
from app.db import Base

# Define the Expense model:
class Expense(Base):
    __tablename__ = "expenses"
    
    id = Column(Integer, primary_key = True, index = True)
    amount = Column(Float, nullable = False)
    category = Column(String, nullable = False)
    date = Column(Date, nullable = False)
    description = Column(String)
    payment_method = Column(String)
    merchant = Column(String)
    is_recurring = Column(Boolean, default = False)