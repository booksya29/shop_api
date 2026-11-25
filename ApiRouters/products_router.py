from fastapi import APIRouter, Request
from schemes import Product
from database_control import add_new_products
router = APIRouter()


@router.post(path="/add", status_code=201, tags=["products"])
def add_new(request:Request, data:Product):
    conn = request.app.state.conn
    return add_new_products(conn, data)