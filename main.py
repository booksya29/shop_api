from fastapi import FastAPI, Request, status, HTTPException
from contextlib import asynccontextmanager
from database import connect_db
from database_control import UsersDatabase
from schemes import NewUser
from ApiRouters import user_router, products_router, transactions_router
@asynccontextmanager
async def lifespan(app:FastAPI):
    app.state.conn = connect_db()
    try:
        yield
    finally:
        app.state.conn.close()

app = FastAPI(lifespan=lifespan)
app.include_router(user_router.router, prefix = "/user")
app.include_router(products_router.router, prefix= '/products')
app.include_router(transactions_router.router, prefix="/transactions")

@app.get("/")
def standart():
    return "https://github.com/booksya29/shop_api"