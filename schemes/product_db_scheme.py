from pydantic import BaseModel

class Product(BaseModel):
    id:int | None = None
    barcode:str
    user_id:int
    name:str
    price:float
    count:int
    description:str|None = None