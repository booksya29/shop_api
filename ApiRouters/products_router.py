from fastapi import APIRouter, Request
from schemes import Product
from database_control import add_new_products, view_all_products
router = APIRouter(prefix="")


@router.post(path="/add", status_code=201, tags=["products"])
def add_new(request:Request, data:Product):
    conn = request.app.state.conn
    return add_new_products(conn, data)

@router.get("/", status_code=200, tags=["products"])
def view(request:Request):
    conn = request.app.state.conn
    return view_all_products(conn)