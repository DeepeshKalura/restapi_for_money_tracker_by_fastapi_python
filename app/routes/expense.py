from fastapi import HTTPException, Response, status, Depends, APIRouter
from .. import model, schemas, utils, oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List
from sqlalchemy import text

router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"],
)

@router.get("/")
async def get_all_expenses(db: Session = Depends(get_db)):
        
        raw_sql = """
DROP VIEW IF EXISTS user_category_transaction_amounts;
DROP VIEW IF EXISTS user_category_latest_expenses;

CREATE VIEW user_category_transaction_amounts AS
SELECT
    tr.user_id,
    e.category_id,
    SUM(tr.transaction_amount) AS transaction_amount
FROM
    transactions tr
JOIN expenses e ON tr.transaction_id = e.transaction_id
GROUP BY
    tr.user_id, e.category_id;


CREATE VIEW user_category_latest_expenses AS
SELECT DISTINCT ON (user_id, category_id)
    user_id,
    category_id,
    expense_category
FROM
    expenses
ORDER BY
    user_id, category_id, expense_id DESC;


WITH LatestTransactionDates AS (
    SELECT
        c.category_id,
        MAX(t.transaction_date) AS latest_transaction_date
    FROM
        categories c
    LEFT JOIN expenses e ON c.category_id = e.category_id
    LEFT JOIN transactions t ON e.transaction_id = t.transaction_id
    GROUP BY
        c.category_id
)
SELECT
    c.category_name AS Expense,
    COALESCE(t.transaction_amount, 0) AS Amount,
    CASE WHEN e.expense_category IS NULL THEN 0 ELSE CAST(e.expense_category AS INTEGER) END AS Category,
    COALESCE(l.latest_transaction_date, '1900-01-01'::DATE) AS Date
FROM
    categories c
LEFT JOIN user_category_transaction_amounts t ON c.category_id = t.category_id
LEFT JOIN user_category_latest_expenses e ON c.category_id = e.category_id
LEFT JOIN LatestTransactionDates l ON c.category_id = l.category_id;


 """
        result = db.execute(text(raw_sql))

            
    
        rows = result.fetchall()
        
        # Format the data into the desired output structure
        formatted_data = []
        for row in rows:
            formatted_data.append({
                "expense": row[0],
                "amount": row[1],
                "category": row[2],
                "date": row[3].strftime('%Y-%m-%d') if row[3] else "1900-01-01"
            })
        
        return formatted_data



@router.post("/{categories_id}", status_code=status.HTTP_201_CREATED, response_model=schemas.Expense)
async def create_expense(
    categories_id: int,
    expense_table: schemas.ExpenseCreate,
    current_user: model.User = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db)
):
    # Create a new transaction entry
    new_transaction = model.Transaction(
        user_id=current_user.user_id,
        transaction_amount=expense_table.amount,
    )
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    # Create a new expense entry related to the new transaction
    new_expense = model.Expense(
        user_id=current_user.user_id,
        expense_name=expense_table.expense_name,
        category_id=categories_id,
        transaction_id=new_transaction.transaction_id,
        expense_category = expense_table.expense_category,
        expense_description=expense_table.expense_description
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    
    categories = db.query(model.Category).filter(model.Category.category_id == categories_id).first()
    

    if categories is not None:
        return {
            "expense_name": new_expense.expense_name,
            "amount": new_transaction.transaction_amount,
            "transaction_date": new_transaction.transaction_date,
            "category_id": categories.category_id,
            "category": categories.category_name,
        }
    else:
        raise HTTPException(status_code=404, detail="Category not found")

