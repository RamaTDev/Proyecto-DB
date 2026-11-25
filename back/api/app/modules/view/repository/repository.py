

from psycopg import Error
from typing import List

from app.config.database import DataBaseException, Database
from app.modules.view.repository.irepository import IViewRepository
from app.modules.view.schema import View, ViewFilter


class ViewRepository(IViewRepository):


    _db : Database;

    def __init__(self, db : Database) -> None:
        self._db = db;


    def filter(self, viewFilter: ViewFilter) -> List[View]:

        res : List[View]  = [];

        try:

            sql : str = 'select * from fn_filterView(%s,%s,%s,%s,%s,%s,%s)';

            params = (
                viewFilter.productname,
                viewFilter.categoryname,
                viewFilter.discontinued,
                viewFilter.stockmin,
                viewFilter.stockmax,
                viewFilter.pricemin,
                viewFilter.pricemax
            );


            rows = self._db.execute(sql,params);


            if rows is not None:

                for r in rows:
                    res.append(View(**r));


        except Error as e:
            msg = e.diag.message_primary or 'Error en la base de datos';
            raise DataBaseException(message=msg);
            

        return res;

        

