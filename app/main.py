from fastapi import FastAPI
from .routes import  user, auth, cors, expense

# I added alemic to create tables
#? sqlalchemy_model.Base.metadata.create_all(bind=engine) 
# #! This line not need because I am using alembic to create table 

app = FastAPI()
cors.add_cors(app)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(expense.router)



@app.get("/", tags=["Root"])
async def root():
    return {"message": "Hello World"}   