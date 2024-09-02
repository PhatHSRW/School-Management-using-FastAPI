from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from enum import Enum
from typing import Optional


class Category(Enum):
    TOOLS = "tools"
    CONSUMABLES = "consumables"


class MyItem(BaseModel):
    name: str
    price: float
    num_onstock: int
    category: Category | str
    description: Optional[str] = None


class ItemSell(BaseModel):
    name: str
    num_sell : int = 1


app = FastAPI()

ITEMS = []

@app.get("/")
def root():
    return "Hello my friend!"

@app.get("/items")
def get_items():
    return ITEMS

@app.get("/items/id/{item_id}")
def get_item(item_id: int):
    if item_id < len(ITEMS):
        return ITEMS[item_id]
    else:
        raise HTTPException(status_code=404, detail="Item not found")
    
@app.get("/items/name/{item_name}")
def get_item(item_name: str):
    for item in ITEMS:
        if str.lower(item.name) == str.lower(item_name):
            return item
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@app.get("/items")
def query_item_by_parameters(
    name: str | None = None,
    price: float | None = None,
    num_onstock: int | None = None
):
    return 0

@app.post("/add-item")
def add_item(item : MyItem):
    if len(ITEMS) > 0:
        for item_check in ITEMS:
            if item.name == item_check.name:
                item_check.num_onstock += item.num_onstock
                return f"Saved item {item.name} successfully."
        ITEMS.append(item)
        return f"Saved item {item.name} successfully."
    else:
        ITEMS.append(item)
        return f"Saved item {item.name} successfully."
    
@app.put("/sell-item/{item_sell_name}/{number_sell}")
def sell_item(item_sell_name, number_sell):
    item_sell = ItemSell(name=str.lower(item_sell_name), num_sell=int(number_sell))
    if len(ITEMS) == 0:
        raise HTTPException(status_code=404, detail="Item list is empty")
    for item_check in ITEMS:
        if item_sell.name == str.lower(item_check.name):
            if item_check.num_onstock >= item_sell.num_sell:
                item_check.num_onstock -= item_sell.num_sell
                return f"Sell {number_sell} item(s) {item_check.name} successfully."
            else:
                raise HTTPException(status_code=404, detail="Not enough item on stock.")
            
    raise HTTPException(status_code=404, detail="Item not found.")

 