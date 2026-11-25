

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.config.database import DataBaseException, Database
from app.modules.products.repository.repository import ProductRepository
from app.modules.products.router import ProductRouter
from app.modules.view.repository.repository import ViewRepository
from app.modules.view.router import ViewRouter

app = FastAPI(title='Produdcts');


""" DATABASE """
database = Database();
database.connect();


""" REPOSITORIES """
productRepository = ProductRepository(database);
viewRepository = ViewRepository(database);


""" ROUTERS """
productRouter = ProductRouter(productRepository);
viewRouter = ViewRouter(viewRepository);


""" ENDPOINTS """
app.include_router(productRouter.router,prefix='/products');
app.include_router(viewRouter.router,prefix='/view');



""" HANDLER ERRORS """
@app.exception_handler(DataBaseException)
async def database_exception_handler(request: Request, exc: DataBaseException) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={
            "detail": exc.message
        }
    )