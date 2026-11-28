from fastapi import APIRouter, Request, status, HTTPException
from database_control import UsersDatabase 
from schemes import NewUser, EditUser
from psycopg2.extras import RealDictCursor
router = APIRouter()


@router.post(path="", status_code=status.HTTP_201_CREATED, tags=["Users"])
def add_new_user(request:Request, data:NewUser):
    return (UsersDatabase.add_new_user(request.app.state.conn, data))

@router.patch('/{user_id}', status_code=status.HTTP_202_ACCEPTED, tags=["Users"])
def edit_user_info(request:Request, data:EditUser, user_id:int):
    if user_id == None:
        raise HTTPException(status_code=404, detail="User not found")
    data.id = user_id
    conn = request.app.state.conn
    return UsersDatabase.update_user_info(conn, data)

@router.delete('/{user_id}', status_code=202, tags=["Users"])
def delete_user(request:Request, user_id):
    conn = request.app.state.conn
    return UsersDatabase.delete_user(conn, user_id)


@router.get("", status_code=200, tags=["Users"])
def check_db_state(request:Request, user_id:int = 0):

    cursor = request.app.state.conn.cursor(cursor_factory = RealDictCursor)
    cursor.execute("SELECT * FROM users WHERE (0 = %s OR id = %s)", (user_id, user_id))
    data = cursor.fetchall()
    return data


