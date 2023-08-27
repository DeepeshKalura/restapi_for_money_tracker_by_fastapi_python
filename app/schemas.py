from datetime import datetime, date
from pydantic import BaseModel
from typing import List, Optional


class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str
    name: str

class User(UserBase):
    user_id: int
    name: str
    date_created: datetime

    class Config:
        from_attributes = True
        
class UserUpdate(UserBase):
    password: Optional[str] = None
    name: Optional[str] = None

class ExpenseBase(BaseModel):
    expense_name: str
    category_id: int

class ExpenseCreate(BaseModel):
    expense_name: str
    expense_category : str
    amount: float
    expense_description: Optional[str] = None

class Expense(ExpenseBase):
    amount: int
    transaction_date: date
    category: str

    

    class Config:
        from_attributes = True

class TransactionBase(BaseModel):
    transaction_date: str

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    transaction_id: int
    user: User
    expense: Expense

    class Config:
        from_attributes = True

class CategoryBase(BaseModel):
    category_name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    category_id: int
    expenses: List[Expense] = []

    class Config:
        from_attributes = True


# ! login


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None