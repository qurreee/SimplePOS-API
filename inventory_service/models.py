from pydantic import BaseModel

class InventoryItem(BaseModel):
    product_id: int
    stock: int