from pydantic import BaseModel

# Pydantic schema for Address object
class Address(BaseModel):
    name: str
    city: str
    state: str
    pincode: str
    latitude: str
    longitude: str