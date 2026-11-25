from schemes import NewUser, EditUser, User
from fastapi import HTTPException

class UsersDatabase:
    @staticmethod
    def add_new_user(conn, data:NewUser):
        cursor = conn.cursor()
        cursor.execute("SELECT EXISTS(SELECT 1 FROM users WHERE name = %s)", (data.name,))
        if cursor.fetchone()[0]:
            raise HTTPException(status_code = 409, detail="User already exists")
        else:
            cursor.execute("INSERT INTO users(name, born_year, budget) VALUES(%s, %s, %s)", (data.name, data.born_year, data.budget))
            conn.commit()
        return {
            "status":"Success",
            "message":"User successfully added",
            "user":data.model_dump()
        }
    @staticmethod
    def update_user_info(conn, new_user:EditUser):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s", (new_user.id,))
        data = cursor.fetchone()
        if data is None:
            raise HTTPException(status_code=404, detail="User not found")
        old = User(*data)
        old_data = old.model_dump()
        new_data = new_user.model_dump()
        updated_data = {key:value if value is not None else old_data[key] for key, value in new_data.items()}
        new_user = User(**updated_data)
        cursor.execute("UPDATE users SET name = %s, born_year = %s, budget = %s WHERE id = %s", (new_user.name, new_user.born_year, new_user.budget, new_user.id))
        conn.commit()
        return {
            'status': 200,
            "detail": "Succefull edit",
            'user': new_user.model_dump()
        }