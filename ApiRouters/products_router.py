from fastapi import APIRouter, Request
from schemes import Product
from database_control import add_new_products, view_all_products, update_product_info, delete_product
router = APIRouter(prefix="")


@router.post(path="/add", status_code=201, tags=["products"])
def add_new(request:Request, data:Product):
    conn = request.app.state.conn
    return add_new_products(conn, data)

@router.get("/", status_code=200, tags=["products"])
def view(request:Request):
    conn = request.app.state.conn
    return view_all_products(conn)

@router.patch("/{barcode}", status_code=202, tags = ['products'])
def patch_product(request:Request, barcode:str, data:Product):
    conn = request.app.state.conn
    return update_product_info(conn, barcode, data)

@router.delete(path ="/{barcode}", status_code=200, tags=['products'])
def delete(request:Request, barcode:str):
    conn = request.app.state.conn
    return delete_product(conn, barcode)
