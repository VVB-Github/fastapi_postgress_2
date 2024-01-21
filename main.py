from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import SessionLocal
import models
from typing import List

app = FastAPI()

class Item(BaseModel):
    id : int
    name :str
    description: str
    price: int
    on_offer: bool
    
    class Config:
        orm_mode: True
    

db = SessionLocal()
  
    
# вывод всех записей
@app.get('/item', response_model=List[Item])
async def get_all():
    items = db.query(models.Item).all()
    return items

# вывод записей по id
@app.get('/item/{item_id}', response_model=Item)
async def get_by_id(item_id:int):
    item = db.query(models.Item).filter(models.Item.id==item_id).first()
    return item

# добавление записи
@app.post('/items')
async def add_item(item:Item):  
    item1 = db.query(models.Item).filter(models.Item.name == item.name).first()
    if item1 is not None:
        raise HTTPException(
            status_code=404,
            detail="Item with such name already exists"
        )
    new_item = models.Item(
        name = item.name,
        price = item.price,
        description = item.description,
        on_offer = item.on_offer
    )
        
    db.add(new_item)
    db.commit()
    return {"message":"Item added successfully"}

# модификация записи
@app.put('/item/{item_id}', response_model=Item)
async def modify_item(item_id:int, item:Item):
    item_to_modify = db.query(models.Item).filter(models.Item.id == item_id).first()
    if item_to_modify is None:
        raise HTTPException(
            status_code=404,
            detail="Item with such id do not exists"
        )
    item_to_modify.name = item.name
    item_to_modify.description = item.description
    item_to_modify.price = item.price
    item_to_modify.on_offer = item.on_offer
    return item_to_modify
    

# удаление записи
@app.delete('/item/{item_id}')
async def delete_item(item_id:int):
    item_to_delete = db.query(models.Item).filter(models.Item.id == item_id).first()
    db.delete(item_to_delete)
    return {"message":"item deleted"}