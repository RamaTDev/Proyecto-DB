

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

class SupplierUpdate(BaseModel):
    
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



class SupplierID(BaseModel):

    supplierid: int