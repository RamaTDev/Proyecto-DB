

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.config.database import DataBaseException, Database
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


""" ROUTERS """
productRouter = ProductRouter(productRepository);
supplierRouter = SupplierRouter(supplierRepository);


""" ENDPOINTS """
app.include_router(productRouter.router,prefix='/products');
app.include_router(supplierRouter._router,prefix='/suppliers');



""" HANDLER ERRORS """
@app.exception_handler(DataBaseException)
async def database_exception_handler(request: Request, exc: DataBaseException) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={
            "detail": exc.message
        }
    )

