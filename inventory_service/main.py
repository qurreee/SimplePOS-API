from fastapi import FastAPI,HTTPException
from typing import List
from .models import InventoryItem, StockUpdate
from .data import inventory
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Inventory Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          
    allow_credentials=True,
    allow_methods=["*"],    
    allow_headers=["*"],          
)

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
def reduce_stock(product_id: int, update: StockUpdate):
    qty = update.qty
    for item in inventory:
        if item.product_id == product_id:
            if item.stock < qty:
                raise HTTPException(status_code=400, detail="stock not enough")
            item.stock -= qty
            return {
                "message": "Stock Updated",
                "product_id": product_id,
                "remaining_stock": item.stock
            }
    raise HTTPException(status_code=404, detail="item not found")


@app.put("/inventory/{product_id}/increase", response_model=dict)
def increase_stock(product_id: int, update: StockUpdate):
    qty = update.qty

    for item in inventory:
        if item.product_id == product_id:
            item.stock += qty
            return {
                "message": "Stock Updated",
                "product_id": product_id,
                "new_stock": item.stock
            }

    raise HTTPException(status_code=404, detail="item not found")
