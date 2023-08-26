from fastapi import FastAPI
from .routes import cors

from .database import  engine
from . import  sqlalchemy_model 

sqlalchemy_model.Base.metadata.create_all(bind=engine)

app = FastAPI()
cors.add_cors(app)

@app.get("/expenses", tags=["Expenses"])
async def get_expenses():
    return {"message": "Expenses"}




@app.get("/", tags=["Root"])
async def root():
    return {"message": "Hello World"}   