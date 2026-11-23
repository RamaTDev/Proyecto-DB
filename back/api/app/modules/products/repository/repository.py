

from typing import List

from psycopg import Error
from psycopg.rows import dict_row

from app.config.database import Database, DataBaseException
from app.modules.products.repository.irepository import IProductRepository
from app.modules.products.schemas import Product, ProductID, ProductCreate, ProductUpdate


class ProductRepository(IProductRepository):

    _db : Database;

    def __init__(self,database: Database) -> None:
        self._db = database;
        

    def findAll(self) -> List[Product]:  # type: ignore 

        products : List[Product] = [];

        try:
            sql : str = 'select * from products';
            rows = self._db.execute(sql);
            if rows is not None:
                for r in rows:
                    products.append(Product(**r));
            
        except Error as e:
            clean_msg = e.diag.message_primary or 'Error en la base de datos';
            raise DataBaseException(message=clean_msg) from e;

        return products;
        

  
    def findById(self, product: ProductID) -> Product | None :

        prod : Product | None = None;

        try:
            sql: str = 'select * from fn_getproductbyid(%s)';
            row = self._db.execute_one(sql,(product.productid,))

            if row is not None:
                prod = Product(**row);
        
        except Exception as e:
            return None

        return prod;

        

    def save(self, product : ProductCreate) -> Product | None:

        prod : Product | None = None;

        try:

            sql : str = 'select * from fn_insertProduct( (%s), (%s), (%s), (%s), (%s), (%s), (%s), (%s) )';

            params = (product.productname,
                      product.supplierid,
                      product.categoryid,
                      product.quantityperunit,
                      product.unitprice,
                      product.unitsinstock,
                      product.unitsonorder,
                      product.reorderlevel,
                    );

            row = self._db.execute_one(sql,params);

            if row is not None:
                prod = Product(**row);

        except Error as e:
            msg = e.diag.message_primary or 'Error en la base de datos';
            raise DataBaseException(message=msg);

        return prod;

   
    def delete(self, product : ProductID) -> Product | None:
        prod : Product | None = None;

        try:
            sql : str = 'select * from fn_deleteproduct(%s)';
            row = self._db.execute_one(sql,(product.productid,));

            if row is not None:
                prod = Product(**row);

        except Error as e:
            msg = e.diag.message_primary or 'Error en la base de datos';
            raise DataBaseException(message=msg);

        return prod;
        


    def update(self, productid: ProductID,  product : ProductUpdate) -> Product | None:

        prod : Product | None = None

        try:

            sql : str = 'select * from fn_updateProduct( (%s), (%s), (%s), (%s), (%s), (%s), (%s), (%s), (%s), (%s) )';

            params = (
                      productid.productid,
                      product.productname,
                      product.supplierid,
                      product.categoryid,
                      product.quantityperunit,
                      product.unitprice,
                      product.unitsinstock,
                      product.unitsonorder,
                      product.reorderlevel,
                      product.discontinued);

            row = self._db.execute_one(sql,params);

            if row is not None:

                prod = Product(**row);

        except Error as e:
            msg = e.diag.message_primary or 'Error en la base de datos';
            raise DataBaseException(message=msg);


        return prod;


