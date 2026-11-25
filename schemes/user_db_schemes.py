from pydantic import BaseModel


class NewUser(BaseModel):
    name:str
    born_year:int
    budget:float = 0

class EditUser(BaseModel):
    id:int | None = None
    name:str| None = None
    born_year:int | None = None
    budget:float | None = None

    
class User(BaseModel):
    id: int
    name: str | None = None
    born_year: int | None = None
    budget: float | None = None

    def __init__(self, id, name=None, born_year=None, budget=None):
        super().__init__(
            id=id,
            name=name,
            born_year=born_year,
            budget=budget
        )