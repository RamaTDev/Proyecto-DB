

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

    stockmin : int | None = Field(None, ge=0 , description='stock menores a un limite ');

    stockmax : int | None = Field(None, ge=0, description='stock mayores a un limite');

    pricemin : Decimal | None = Field(None,ge=0,description='precios menores o iguales a un limite');

    pricemax : Decimal | None  = Field(None,ge=0, description='precios mayores o iguales a un limite');

