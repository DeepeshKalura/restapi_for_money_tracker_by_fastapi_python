from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

from .database import Base

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    name = Column(String)
    date_created = Column(DateTime(timezone=True), server_default=func.now())

    expenses = relationship("Expense", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")

class Expense(Base):
    __tablename__ = 'expenses'

    expense_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    expense_name = Column(String)
    amount = Column(Float)
    category_id = Column(Integer, ForeignKey('categories.category_id'))
    latest_transaction_date = Column(Date)

    user = relationship("User", back_populates="expenses")
    transactions = relationship("Transaction", back_populates="expense")

class Transaction(Base):
    __tablename__ = 'transactions'

    transaction_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    expense_id = Column(Integer, ForeignKey('expenses.expense_id'))
    transaction_date = Column(Date)

    user = relationship("User", back_populates="transactions")
    expense = relationship("Expense", back_populates="transactions")

class Category(Base):
    __tablename__ = 'categories'

    category_id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String)
    
    expenses = relationship("Expense", back_populates="category")
