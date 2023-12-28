from pydantic import BaseModel

class Temperature(BaseModel):
    id: int
    device_name: str
    temperature: float