from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class UserModel(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    baskets = relationship("BasketModel", back_populates="user")

class BasketModel(Base):
    __tablename__ = 'baskets'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship("UserModel", back_populates="baskets")
    items = relationship("ItemModel", back_populates="basket", cascade="all, delete-orphan")

class ItemModel(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, index=True)
    basket_id = Column(Integer, ForeignKey('baskets.id'), nullable=False)
    name = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)

    basket = relationship("BasketModel", back_populates="items")