

from  decimal import Decimal

from pydantic import BaseModel


class View(BaseModel):

    productid: int

    producto: str 

    precio: Decimal 

    stock: int

    categoria: str

    proveedor: str

    discontinuado: bool


class ProductName(BaseModel):

    name : str


class CategoryName(BaseModel):

    name: str


class Stock(BaseModel):

    stock: int


class StockRange(BaseModel):

    gt : int

    lt : int


 