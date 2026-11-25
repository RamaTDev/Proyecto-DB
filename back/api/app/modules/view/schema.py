

from  decimal import Decimal

from pydantic import BaseModel, Field


class View(BaseModel):

    productid: int 

    product: str 

    price: Decimal 

    stock: int

    category: str

    supplier: str

    discontinued: bool

    active: bool


class ViewFilter(BaseModel):

    productname : str | None = Field(None, description='Filtra por nombre de producto');

    categoryname : str | None = Field(None, description='Filtra por nombre de categoria');

    discontinued : bool | None = Field(None, description='Filtra por descontinuados o no');

    stockmin : int | None = Field(None, ge=0 , description='Filtra por productos con stock menores o iguales')

    stockmax : int | None = Field(None, ge=0, description='Filtra por productos con stock mayores o iguales')

    pricemin : Decimal | None = Field(None,ge=0,description='Filtra por precios menores o iguales')

    pricemax : Decimal | None  = Field(None,ge=0, description='Filtra por precios mayores o iguales ')

