

from abc import abstractmethod
from typing import List

from psycopg import Error

from app.config.database import DataBaseException, Database
from app.modules.suppliers.repository.irepository import ISupplierRepository
from app.modules.suppliers.schemas import Supplier, SupplierCreate, SupplierID, SupplierUpdate


class SupplierRepository(ISupplierRepository):


    _db : Database;

    def __init__(self, db : Database) -> None:
        self._db = db;
           

    def findAll(self) -> List[Supplier] | List:
            
        suppliers : List[Supplier] = [];

        try:

            sql : str = 'select * from suppliers';
            rows = self._db.execute(sql);
            if rows is not None:

                for r in rows:
                    suppliers.append(Supplier(**r));

        except Error as e:
            msg = e.diag.message_primary or 'Error en la base de datos';
            raise DataBaseException(message=msg);
    

        return suppliers;

            
    
    def findById(self, supplierid : SupplierID) -> Supplier | None:

        supplier : Supplier | None = None;
    
        try:
    
            sql : str = 'select * from suppliers s where s.supplierid = (%s)';
            row = self._db.execute_one(sql,(supplierid.supplierid,));
            if row is not None:
               supplier = Supplier(**row);
            else:
                return None;
            
        except Error as e:
            msg = e.diag.message_primary or 'Error en la base de datos';
            raise DataBaseException(message=msg);
        
    
        return supplier;
    
    
    def save(self, supplier : SupplierCreate) -> Supplier | None:

        res : Supplier | None = None;
            
        try:
            sql : str = 'select * from fn_insertsupplier(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)';
            params = (
                supplier.companyname,
                supplier.contactname,
                supplier.contacttitle,
                supplier.address,
                supplier.city,
                supplier.region,
                supplier.postalcode,
                supplier.country,
                supplier.phone,
                supplier.fax,
                supplier.homepage
            )
            row = self._db.execute_one(sql,params);
            if row is not None:
                res = Supplier(**row);
            else:
                return None;
                    
        except Error as e:
            msg = e.diag.message_primary or 'Error en la base de datos';
            raise DataBaseException(message=msg);
                
            
        return res;
    
    
    def update(self, supplierid: SupplierID, supplier: SupplierUpdate ) -> Supplier | None:
        res : Supplier | None = None;
                 
        try:
            sql : str = 'select * from fn_updatesupplier(%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)';
                 
            params = (
                supplierid.supplierid,
                supplier.companyname,
                supplier.contactname,
                supplier.contacttitle,
                supplier.address,
                supplier.city,
                supplier.region,
                supplier.postalcode,
                supplier.country,
                supplier.phone,
                supplier.fax,
                supplier.homepage
            )

            row = self._db.execute_one(sql,params);
            if row is not None:
                res = Supplier(**row);
            else:
                return None;
                         
        except Error as e:
            msg = e.diag.message_primary or 'Error en la base de datos';
            raise DataBaseException(message=msg);
                     
                 
        return res;
    
    
    def delete(self, supplierid: SupplierID) -> Supplier | None:

        supplier : Supplier;

        try:

            sql: str = 'select * from fn_deletesupplier(%s)';
            row = self._db.execute_one(sql,(supplierid.supplierid,));

            if row is not None:
                supplier = Supplier(**row);
            else:
                return None

        except Error as e:
            msg = e.diag.message_primary or 'Eror en la base de datos';
            raise DataBaseException(message=msg);

        return supplier;
    
    
    def activate(self, supplierid: SupplierID) -> Supplier | None:
        supplier : Supplier;
        
        try:
        
            sql: str = 'select * from fn_activatesupplier(%s)';
            row = self._db.execute_one(sql,(supplierid.supplierid,));
        
            if row is not None:
                supplier = Supplier(**row);
            else:
                return None
        
        except Error as e:
                msg = e.diag.message_primary or 'Eror en la base de datos';
                raise DataBaseException(message=msg);
        
        return supplier;
    
    
    
    
    