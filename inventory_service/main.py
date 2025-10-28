from fastapi import FastAPI,HTTPException
from typing import List
from .models import InventoryItem
from .data import inventory

app = FastAPI(title="Inventory Service")

@app.get("/inventory", response_model= List[InventoryItem])
def get_inventory():
    return inventory

@app.get("/inventory/{product_id}", response_model=InventoryItem)
def get_item(product_id: int):
    for item in inventory:
        if item.product_id == product_id:
            return item
    raise HTTPException(status_code=404, detail="Item not Found!")

@app.post("/inventory", response_model=InventoryItem)
def add_item(item: InventoryItem):
    if any(i.product_id == item.product_id for i in inventory):
        raise HTTPException(status_code=400, detail="item already exist")
    inventory.append(item)
    return item

@app.put("/inventory/{product_id}/reduce")
def reduce_stock(product_id: int, qty: int):
    for item in inventory:
        if item.product_id == product_id:
            if item.stock < qty:
                raise HTTPException(status_code=400, detail="stock not enough")
            item.stock -= qty
            return {"message": "Stock Updated", "product_id": product_id, "remaining_stock":item.stock}
    raise HTTPException(status_code=404, detail="item not found")

@app.put("/inventory/{product_id}/increase")
def increase_stock(product_id: int, qty: int):
    for item in inventory:
        if item.product_id == product_id:
            item.stock += qty
            return {"message": "Stock increased", "product_id": product_id, "new_stock": item.stock}
    raise HTTPException(status_code=404, detail="Item not found")