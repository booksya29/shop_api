from schemes import Transaction, AddTrascationModel
from fastapi import status, HTTPException
from schemes import EditUser
from psycopg2.extras import RealDictCursor
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
    added_data = cursor.fetchone()
    conn.commit()
    cursor.close()
    return {
        "status":200,
        'transaction':added_data
    }

def get_list_of_transactions(conn, buyer_id:int):
    cursor = conn.cursor(cursor_factory = RealDictCursor)
    cursor.execute("SELECT users.name AS user_name, products.name, transactions.b_change, transactions.date FROM transactions INNER JOIN users ON users.id = transactions.buyer_id INNER JOIN products ON products.barcode = transactions.product_barcode WHERE (%s = 0 OR transactions.buyer_id = %s)", (buyer_id, buyer_id))
    return {
        "status": 200,
        "history": cursor.fetchall()
    }