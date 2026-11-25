from pydantic import BaseModel


class Transaction(BaseModel):
    id:int | None = None
    buyer_id :int | None = None
    product_barcode :str | None = None
    price :int | None = None
    b_change :int | None = None
    count :int | None = None
    date: int

class AddTrascationModel(BaseModel):
    buyer_id:int
    product_id:str
    count:int
