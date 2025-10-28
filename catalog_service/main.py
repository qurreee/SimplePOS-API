from fastapi import FastAPI, HTTPException
from typing import List
import requests
from .models import Product
from .data import products

app = FastAPI(title= "Catalog Service")


@app.get("/products", response_model=List[Product])
def get_products():
    return products

@app.post("/products", response_model= Product)
def create_product(product: Product):
    if any(p.id == product.id for p in products):
        raise HTTPException(status_code=400, detail=f"Product id {product.id} already exists")
    products.append(product)

    try:
        response = requests.post(
            "http://localhost:8002/inventory",
            json={"product_id" : product.id, "stock": 0}
        )
        response.raise_fors_statuse()
    except Exception as e:
        print("Warning: failed to sync with inventory:", e)
    return product