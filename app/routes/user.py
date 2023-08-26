from fastapi import HTTPException, Response, status, Depends, APIRouter
from .. import sqlalchemy_model, schemas, utils, oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


#? Currently I does not wanted to get user becasue one user can't communicate with other user


# ! Just for the testing purpose
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.User])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(sqlalchemy_model.User).all()
    return users





@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Has the password hashed - user.password
    checking_user = db.query(sqlalchemy_model.User).filter(sqlalchemy_model.User.email == user.email).first()
    if checking_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email {user.email} already exists",
        )
    hash = utils.hash(user.password)
    user.password = hash
    new_user = sqlalchemy_model.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user




@router.patch("/", response_model=schemas.User)
def update_user(user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    user = db.query(sqlalchemy_model.User).filter(sqlalchemy_model.User.email == user_update.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email {user_update.email} not found",
        )

    if not user_update.password and not user_update.name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field (password or name) must be provided for update",
        )

    if user_update.password:
        hash = utils.hash(user_update.password)
        user.password = hash

    if user_update.name:
        user.name = sqlalchemy_model.Column(sqlalchemy_model.String, default=user_update.name)

    db.commit()
    db.refresh(user)  

    return user  
