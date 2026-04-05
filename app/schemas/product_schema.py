from pydantic import BaseModel
from typing import Optional


class ProductBase(BaseModel):
    name: str
    price: float
    cost_price: Optional[float] = 0.0
    stock: int
    barcode: Optional[str] = None
    category: Optional[str] = None 
    supplier: Optional[str] = None
    low_stock_threshold: Optional[int] = 10
    image: Optional[str] = None
    


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    cost_price: Optional[float] = None
    stock: Optional[int] = None
    barcode: Optional[str] = None
    supplier: Optional[str] = None
    low_stock_threshold: Optional[int] = None
    image: Optional[str] = None
    
class LowStockProductResponse(BaseModel):
    name: str
    stock: int
    low_stock_threshold: Optional[int] = None


class ProductResponse(ProductBase):
    id: str 

    class Config:
        # This allows the model to work with MongoDB dictionaries
        from_attributes = True 
        populate_by_name = True