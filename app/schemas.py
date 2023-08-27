from datetime import datetime
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
    amount: float
    category_id: int

class ExpenseCreate(ExpenseBase):
    pass

class Expense(ExpenseBase):
    expense_id: int
    latest_transaction_date: str
    user: User

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