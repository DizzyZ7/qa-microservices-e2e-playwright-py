from pydantic import BaseModel, ConfigDict, Field, field_validator


class OrderCreate(BaseModel):
    item: str = Field(min_length=3, max_length=120)

    @field_validator("item")
    @classmethod
    def normalize_item(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("Item must not be blank")
        return normalized


class OrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    item: str
    status: str
