

from decimal import Decimal

from pydantic import BaseModel, Field


class Product(BaseModel): 

    productid : int

    productname : str

    supplierid : int

    categoryid :int

    quantityperunit : str

    unitprice : Decimal

    unitsinstock : int

    unitsonorder : int

    reorderlevel : int

    discontinued : bool

    active : bool

class ProductCreate(BaseModel):

    productname : str | None;
    
    supplierid : int | None
    
    categoryid :int | None
    
    quantityperunit : str | None
    
    unitprice : Decimal | None
    
    unitsinstock : int | None
    
    unitsonorder : int | None
    
    reorderlevel : int | None


class ProductUpdate(BaseModel):

    productname : str | None

    supplierid : int | None

    categoryid :int | None

    quantityperunit : str | None

    unitprice : Decimal | None

    unitsinstock : int | None

    unitsonorder : int | None

    reorderlevel : int | None

    discontinued : bool | None


class ProductID(BaseModel):
     
    productid : int


