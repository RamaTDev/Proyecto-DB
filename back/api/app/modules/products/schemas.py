

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


class ProductID(BaseModel):
     
    productid : int


class ProductCreate(BaseModel):

     productname : str
    
     supplierid : int
    
     categoryid :int
    
     quantityperunit : str
    
     unitprice : Decimal
    
     unitsinstock : int
    
     unitsonorder : int
    
     reorderlevel : int
    
     discontinued : bool;





