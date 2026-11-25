

from typing import List

from psycopg import Error
from app.config.database import DataBaseException, Database
from app.modules.categories.repository.irepository import ICategoryRepository
from app.modules.categories.schemas import Category, CategoryCreate, CategoryID


class CategoryRepository(ICategoryRepository):

    _db : Database;

    def __init__(self, db : Database) -> None:
        self._db = db;


    def findAll(self) -> List[Category]:

        categories : List[Category] = [];

        try:

            sql: str = 'select * from categories';

            rows = self._db.execute(sql);

            if rows is not None:
                for r in rows:
                    categories.append(Category(**r));


        except Error as e:
            msg = e.diag.message_primary or 'Error en la base de datos';
            raise DataBaseException(message=msg);
            

        return categories;


    def findById(self, category: CategoryID) -> Category | None:

        res : Category;
        
        try:
        
            sql: str = 'select * from categories c where c.categoryid = %s ';
        
            row = self._db.execute_one(sql,(category.categoryid,));
        
            if row is not None:
               res = Category(**row);
            else:
                return None;
        
        
        except Error as e:
            msg = e.diag.message_primary or 'Error en la base de datos';
            raise DataBaseException(message=msg);
        
        
        return res;

    def save(self, category: CategoryCreate) -> str | None:

        res : str;
        
        try:
        
            sql: str = 'select * from fn_abmr_categorias(%s, %s, %s, %s, %s) as r';
            params = (
                'A',
                None,
                category.categoryname,
                category.description,
                category.picture,
            )
        
            row = self._db.execute_one(sql,params);

            if row is not None:
                res = row['r'];
            else:
                return None;
            
        except Error as e:
            msg = e.diag.message_primary or 'Error en la base de datos';
            raise DataBaseException(message=msg);
        
        
        return res;

        

    def update(self, categoryid: CategoryID, category: CategoryCreate) -> str | None:
        res : str;
        
        try:
        
            sql: str = 'select * from fn_abmr_categorias(%s, %s, %s, %s, %s) as r';
            params = (
                'M',
                str(categoryid.categoryid),
                category.categoryname,
                category.description,
                category.picture,
            )
        
            row = self._db.execute_one(sql,params);
        
            if row is not None:
                res = row['r'];
            else:
                return None;
        
        except Error as e:
            msg = e.diag.message_primary or 'Error en la base de datos';
            raise DataBaseException(message=msg);
        
        
        return res;

    def delete(self, categoryid: CategoryID) -> str | None:

        res : str;
        
        try:
            sql: str = 'select * from fn_abmr_categorias(%s, %s, %s, %s, %s) as r';
            params = (
                'B',
                str(categoryid.categoryid),
                None,
                None,
                None,
            )
        
            row = self._db.execute_one(sql,params);
        
            if row is not None:
                res = row['r'];
            else:
                return None;
        
        except Error as e:
            msg = e.diag.message_primary or 'Error en la base de datos';
            raise DataBaseException(message=msg);
        
        
        return res;

        

    def activate(self, categoryid: CategoryID) -> str | None:
        res : str;
        
        try:
        
            sql: str = 'select * from fn_abmr_categorias(%s, %s, %s, %s, %s) as r';
            params = (
                'R',
                str(categoryid.categoryid),
                None,
                None,
                None,
            )
        
            row = self._db.execute_one(sql,params);
        
            if row is not None:
                res = row['r'];
            else:
                return None;
        
        except Error as e:
            msg = e.diag.message_primary or 'Error en la base de datos';
            raise DataBaseException(message=msg);
        
        
        return res;


    