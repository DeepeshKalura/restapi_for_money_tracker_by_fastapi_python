from fastapi import FastAPI
from .routes import cors


app = FastAPI()
cors.add_cors(app)





@app.get("/expenses", tags=["Expenses"])
async def get_expenses():
    return {"message": "Expenses"}




@app.get("/", tags=["Root"])
async def root():
    return {"message": "Hello World"}   