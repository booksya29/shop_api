from schemes import Transaction, AddTrascationModel
from fastapi import status, HTTPException
from schemes import EditUser
from database_control import update_product_info, UsersDatabase, Product
from time import time

def add_new_transaction(conn, data:AddTrascationModel):
    cursor = conn.cursor()
    cursor.execute("SELECT count, price FROM products WHERE barcode = %s", (data.product_id,))
    product_count, product_price = cursor.fetchone()
    if product_count < data.count:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No enough products")
    cursor.execute("SELECT budget FROM users WHERE id = %s", (data.buyer_id,))
    user_budget = cursor.fetchone()[0]
    if user_budget < product_price:
        raise HTTPException(status_code=400, detail="Not enough money in user")
    new_product_count = product_count - data.count
    new_user_budget = user_budget - product_price * data.count
    UsersDatabase.update_user_info(conn, EditUser(id=data.buyer_id,budget=new_user_budget))
    update_product_info(conn, data.product_id, Product(count=new_product_count))
    cursor.execute("INSERT INTO transactions(buyer_id, product_barcode, price, b_change, count, date) VALUES (%s,%s,%s,%s,%s,%s) RETURNING *", (data.buyer_id, data.product_id, product_price, float(data.count) * float(product_price), data.count, time()))
    added_data = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    return {
        "status":200,
        'transaction':added_data
    }