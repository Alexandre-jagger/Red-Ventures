from pydantic import BaseModel

class Broth(BaseModel):
    id: str
    imageInactive: str
    imageActive: str
    name: str
    description: str
    price: float

class Protein(BaseModel):
    id: str
    imageInactive: str
    imageActive: str
    name: str
    description: str
    price: float

class OrderRequest(BaseModel):
    brothId: str
    proteinId: str

class OrderResponse(BaseModel):
    id: str
    description: str
    image: str
