from fastapi import status, HTTPException
from psycopg2.extras import RealDictCursor
from schemes import Product

def add_new_products(conn, data:Product):
    cursor = conn.cursor()
    cursor.execute("SELECT EXISTS(SELECT 1 FROM products WHERE barcode = %s)", (data.barcode,))
    exists = cursor.fetchone()[0]
    if exists:
        raise HTTPException(status_code=404, detail="Product already exists")
    cursor.execute("INSERT INTO products(barcode, user_id, name, price, count, description) VALUES(%s,%s,%s,%s,%s,%s)", (data.barcode, data.user_id, data.name, data.price, data.count, data.description))
    conn.commit()
    return {
        'status':status.HTTP_201_CREATED,
        'message':"Successful created",
        'product':data.model_dump()
    }

def view_all_products(conn):
    cursor = conn.cursor(cursor_factory = RealDictCursor)
    cursor.execute("SELECT * FROM products")
    return {
        'status':200,
        "items": cursor.fetchall()
    }