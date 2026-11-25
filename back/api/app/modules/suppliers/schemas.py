

from pydantic import BaseModel


class Supplier(BaseModel):

    supplierid: int

    companyname: str

    contactname: str

    contacttitle: str

    address: str

    city: str

    region: str

    postalcode: str

    country: str

    phone: str

    fax: str

    homepage: str

    active: bool


class SupplierCreate(BaseModel):

    companyname: str | None
    
    contactname: str | None
    
    contacttitle: str | None
    
    address: str | None
    
    city: str | None
    
    region: str | None
    
    postalcode: str | None
    
    country: str | None
    
    phone: str | None
    
    fax: str | None
    
    homepage: str | None

class SupplierUpdate(BaseModel):
    
    companyname: str | None
    
    contactname: str | None
    
    contacttitle: str | None
    
    address: str | None
    
    city: str | None
    
    region: str | None
    
    postalcode: str | None
    
    country: str | None
    
    phone: str | None
    
    fax: str | None
    
    homepage: str | None



class SupplierID(BaseModel):

    supplierid: int