from fastapi import APIRouter, HTTPException, Header, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database import get_db
import models
from schemas.schema import User, Basket, Item

routers = APIRouter()

@routers.post('/users', response_model=User)
def addUser(user: User, db: Session = Depends(get_db)) -> User:
    existing_user = db.query(models.UserModel).filter(models.UserModel.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="A felhasználó már létezik")
    new_user = models.UserModel(name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@routers.post('/baskets')
def addShoppingBag(userid: int, db: Session = Depends(get_db)) -> str:
    user = db.query(models.UserModel).filter(models.UserModel.id == userid).first()
    if not user:
        raise HTTPException(status_code=404, detail="Felhasználó nem található")
    new_basket = models.BasketModel(user_id=userid)
    db.add(new_basket)
    db.commit()
    db.refresh(new_basket)
    return JSONResponse(content={"message": "Shopping bag created successfully", "basket_id": new_basket.id}, status_code=200)

@routers.post('/baskets/{basket_id}/items', response_model=Basket)
def addItem(userid: int, item: Item, db: Session = Depends(get_db)) -> Basket:
    user = db.query(models.UserModel).filter(models.UserModel.id == userid).first()
    if not user:
        raise HTTPException(status_code=404, detail="Felhasználó nem található")
    basket = db.query(models.BasketModel).filter(models.BasketModel.user_id == userid).first()
    if not basket:
        raise HTTPException(status_code=404, detail="Shopping bag not found for the user")
    new_item = models.ItemModel(basket_id=basket.id, name=item.name, brand=item.brand, price=item.price, quantity=item.quantity)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    basket_items = db.query(models.ItemModel).filter(models.ItemModel.basket_id == basket.id).all()
    return Basket(id=basket.id, user_id=userid, items=[Item(item_id=i.id, name=i.name, brand=i.brand, price=i.price, quantity=i.quantity) for i in basket_items])

@routers.put('/items/{itemid}', response_model=Basket)
def updateItem(userid: int, itemid: int, updateItem: Item, db: Session = Depends(get_db)) -> Basket:
    user = db.query(models.UserModel).filter(models.UserModel.id == userid).first()
    if not user:
        raise HTTPException(status_code=404, detail="Felhasználó nem található")
    basket = db.query(models.BasketModel).filter(models.BasketModel.user_id == userid).first()
    if not basket:
        raise HTTPException(status_code=404, detail="Shopping bag not found for the user")
    item = db.query(models.ItemModel).filter(models.ItemModel.id == itemid, models.ItemModel.basket_id == basket.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found in the shopping bag")
    item.name = updateItem.name
    item.brand = updateItem.brand
    item.price = updateItem.price
    item.quantity = updateItem.quantity
    db.commit()
    db.refresh(item)
    basket_items = db.query(models.ItemModel).filter(models.ItemModel.basket_id == basket.id).all()
    return Basket(id=basket.id, user_id=userid, items=[Item(item_id=i.id, name=i.name, brand=i.brand, price=i.price, quantity=i.quantity) for i in basket_items])

@routers.delete('/items/{itemid}', response_model=Basket)
def deleteItem(userid: int, itemid: int, db: Session = Depends(get_db)) -> Basket:
    user = db.query(models.UserModel).filter(models.UserModel.id == userid).first()
    if not user:
        raise HTTPException(status_code=404, detail="Felhasználó nem található")
    basket = db.query(models.BasketModel).filter(models.BasketModel.user_id == userid).first()
    if not basket:
        raise HTTPException(status_code=404, detail="Shopping bag not found for the user")
    item = db.query(models.ItemModel).filter(models.ItemModel.id == itemid, models.ItemModel.basket_id == basket.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found in the shopping bag")
    db.delete(item)
    db.commit()
    basket_items = db.query(models.ItemModel).filter(models.ItemModel.basket_id == basket.id).all()
    return Basket(id=basket.id, user_id=userid, items=[Item(item_id=i.id, name=i.name, brand=i.brand, price=i.price, quantity=i.quantity) for i in basket_items])

@routers.get('/user', response_model=User)
def user(userid: int, db: Session = Depends(get_db)):
    user = db.query(models.UserModel).filter(models.UserModel.id == userid).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@routers.get('/users')
def users(db: Session = Depends(get_db)):
    users = db.query(models.UserModel).all()
    return users
        

@routers.get('/baskets', response_model=list[Basket])
def shoppingBag(db: Session = Depends(get_db), userid: int = None) -> list[Item]:
    if userid is None:
        raise HTTPException(status_code=400, detail="User ID is required")
    shopping_bag = db.query(models.BasketModel).filter(models.BasketModel.user_id == userid).first()
    if not shopping_bag:
        raise HTTPException(status_code=404, detail="Shopping bag not found for the user")
    items = db.query(models.ItemModel).filter(models.ItemModel.basket_id == shopping_bag.id).all()
    return items

@routers.get('/getusertotal')
def getUserTotal(db: Session = Depends(get_db), userid: int = None):
    if userid is None:
        raise HTTPException(status_code=400, detail="User ID is required")
    shopping_bag = db.query(models.BasketModel).filter(models.BasketModel.user_id == userid).first()
    if not shopping_bag:
        raise HTTPException(status_code=404, detail="Shopping bag not found for the user")
    total = sum(item.price * item.quantity for item in shopping_bag.items)
    return round(total, 2)