from pydantic import BaseModel

class OrderCreate(BaseModel):
    item: str

class OrderOut(BaseModel):
    id: int
    item: str
    status: str

    class Config:
        from_attributes = True
