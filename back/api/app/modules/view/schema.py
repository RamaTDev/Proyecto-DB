

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

    product: str | None  = Field(None);
    category: str | None = Field(None);
    discontinued: bool | None = Field(None);


    stock_min: int | None = Field(None,ge=0,description='Stock mayor o igual a 0');
    stock_max: int | None = Field(None,ge=0,description='Stock menot o igual a 0');


    price_min: int | None = Field(None,ge=0,description='Precio mayor o igual a 0');
    price_max: int | None = Field(None,ge=0,description='Precio menor o igual a 0');





 