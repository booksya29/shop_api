from fastapi import FastAPI, Request, status, HTTPException
from contextlib import asynccontextmanager
from database import connect_db
from database_control import UsersDatabase
from schemes import NewUser
from UserApi import user_router
@asynccontextmanager
async def lifespan(app:FastAPI):
    app.state.conn = connect_db()
    try:
        yield
    finally:
        app.state.conn.close()

app = FastAPI(lifespan=lifespan)
app.include_router(user_router.router, prefix = "/user")
@app.get("/")
def check_db_state(request:Request):

    cursor = request.app.state.conn.cursor()
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()
    return data


