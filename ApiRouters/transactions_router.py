from fastapi import APIRouter, Request
from schemes import AddTrascationModel
from database_control import add_new_transaction
router = APIRouter()

@router.post("/new", status_code=200, tags=["transactions"])
def add_new_product(request:Request, data:AddTrascationModel):
    conn = request.app.state.conn
    return add_new_transaction(conn, data)
