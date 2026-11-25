from pydantic import BaseModel

class Product(BaseModel):
    id:int | None = None
    barcode:str |None = None
    user_id:int|None = None
    name:str|None = None
    price:float|None = None
    count:int|None = None
    description:str|None = None