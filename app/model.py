from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date, Float, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

from .database import Base

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False) #? I changed this name from password_hash to password
    name = Column(String)
    date_created = Column(DateTime(timezone=True), server_default=func.now())

   

class Category(Base):
    __tablename__ = 'categories'

    category_id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String)
    description = Column(String)
    

class Transaction(Base):
    __tablename__ = 'transactions'

    transaction_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    transaction_amount = Column(Float, nullable=False)
    # expense_id = Column(Integer, ForeignKey('expenses.expense_id'))
    transaction_date = Column(Date, nullable=False, server_default=func.now())

    # user = relationship("User", back_populates="transactions")
    # expense = relationship("Expense", back_populates="transactions")

class Expense(Base):
    __tablename__ = 'expenses'

    expense_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    expense_name = Column(String)
    # amount = Column(Float)
    category_id = Column(Integer, ForeignKey('categories.category_id'))
    transaction_id = Column(Integer, ForeignKey('transactions.transaction_id'))
    expense_category = Column(String, CheckConstraint('expense_category IN (-1, 0, 1)', name='check_expense_category', ), nullable=False)
    expense_description = Column(String, nullable=False)

    # user = relationship("User", back_populates="expenses")
    # transactions = relationship("Transaction", back_populates="expense")


