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


def update_product_info(conn, barcode:str, data:Product):
    cursor = conn.cursor(cursor_factory = RealDictCursor)
    cursor.execute("SELECT * FROM products WHERE barcode = %s", (barcode,))
    old = cursor.fetchone()
    if not old:
        raise HTTPException(status_code=404, detail="Product not found")
    new = data.model_dump()
    updated = {key:value if value is not None else old[key] for key, value in new.items()}
    print(updated)
    np = Product(**updated)
    cursor.execute("UPDATE products SET user_id = %s, name = %s, price = %s, count = %s, description = %s WHERE barcode = %s", (np.user_id, np.name, np.price, np.count, np.description, np.barcode))
    conn.commit()
    return {
        "status" : 202,
        "message" : "Update product",
        "Product":updated
    }