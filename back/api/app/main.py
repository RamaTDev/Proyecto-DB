

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config.database import DataBaseException, Database
from app.modules.categories.repository.repository import CategoryRepository
from app.modules.categories.router import CategoryRouter
from app.modules.products.repository.repository import ProductRepository
from app.modules.products.router import ProductRouter
from app.modules.view.repository.repository import ViewRepository
from app.modules.view.router import ViewRouter
from app.modules.suppliers.repository.repository import SupplierRepository
from app.modules.suppliers.router import SupplierRouter

app = FastAPI(title='Produdcts');


""" CORS """
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500", "http://localhost:5500",  # Live Server
        "http://127.0.0.1:5173", "http://localhost:5173",  # Vite / React
        "http://127.0.0.1:3000", "http://localhost:3000",  # CRA / Next (opcional)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


""" DATABASE """
database = Database();
database.connect();


""" REPOSITORIES """
productRepository = ProductRepository(database);
viewRepository = ViewRepository(database);
supplierRepository = SupplierRepository(database);
categoryRepository = CategoryRepository(database);


""" ROUTERS """
productRouter = ProductRouter(productRepository);
viewRouter = ViewRouter(viewRepository);
supplierRouter = SupplierRouter(supplierRepository);
categotyRouter = CategoryRouter(categoryRepository);


""" ENDPOINTS """
app.include_router(productRouter.router,prefix='/products');
app.include_router(viewRouter.router,prefix='/view');
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

