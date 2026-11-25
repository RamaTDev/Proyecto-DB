

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


 