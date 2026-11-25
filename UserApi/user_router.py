from fastapi import APIRouter, Request, status, HTTPException
from database_control import UsersDatabase 
from schemes import NewUser, EditUser
router = APIRouter()


@router.post(path="", status_code=status.HTTP_201_CREATED)
def add_new_user(request:Request, data:NewUser):
    return (UsersDatabase.add_new_user(request.app.state.conn, data))

@router.patch('/{user_id}', status_code=status.HTTP_202_ACCEPTED)
def edit_user_info(request:Request, data:EditUser, user_id:int):
    if user_id == None:
        raise HTTPException(status_code=404, detail="User not found")
    data.id = user_id
    conn = request.app.state.conn
    return UsersDatabase.update_user_info(conn, data)

@router.delete('/{user_id}', status_code=202)
def delete_user(request:Request, user_id):
    conn = request.app.state.conn
    return UsersDatabase.delete_user(conn, user_id)