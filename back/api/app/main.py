

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.config.database import DataBaseException, Database
from app.modules.categories.repository.repository import CategoryRepository
from app.modules.categories.router import CategoryRouter
from app.modules.products.repository.repository import ProductRepository
from app.modules.products.router import ProductRouter
from app.modules.suppliers.repository.repository import SupplierRepository
from app.modules.suppliers.router import SupplierRouter

app = FastAPI(title='Produdcts');


""" DATABASE """
database = Database();
database.connect();


""" REPOSITORIES """
productRepository = ProductRepository(database);
supplierRepository = SupplierRepository(database);
categoryRepository = CategoryRepository(database);


""" ROUTERS """
productRouter = ProductRouter(productRepository);
supplierRouter = SupplierRouter(supplierRepository);
categotyRouter = CategoryRouter(categoryRepository);


""" ENDPOINTS """
app.include_router(productRouter.router,prefix='/products');
app.include_router(supplierRouter.router,prefix='/suppliers');
app.include_router(categotyRouter.router,prefix='/categories');



""" HANDLER ERRORS """
@app.exception_handler(DataBaseException)
async def database_exception_handler(request: Request, exc: DataBaseException) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={
            "detail": exc.message
        }
    )

