

from typing import Any, List

from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.modules.products.repository.irepository import IProductRepository
from app.modules.products.schemas import Product, ProductID, ProductCreate


class ProductRouter:

    _router : APIRouter;
    _repository : IProductRepository


    def __init__(self, repository : IProductRepository) -> None:
        self._repository = repository;
        self._router = APIRouter(tags=['products']);
        self._registerRoutes();


    def _registerRoutes(self) -> None:
        self._router.add_api_route('/',self._getProducts,methods=['GET']);
        self._router.add_api_route('/{id}',self._getProductById,methods=['GET']);
        self._router.add_api_route('/',self._createProduct,methods=['POST']);
        self.router.add_api_route('/{id}',self._deleteProduct,methods=['DELETE']);
        self.router.add_api_route('/{id}',self._updateProduct,methods=['PUT']);

    def _getProducts(self) -> JSONResponse:
        products : List[Product] = self._repository.findAll();
        return JSONResponse(content={'products':jsonable_encoder(products)}); 

    def _getProductById(self, id : int) -> JSONResponse:

        product : Product | None = self._repository.findById(ProductID(productid=id));

        if product is not None:
            return JSONResponse(content={'message':'product found', 'product':jsonable_encoder(product)},status_code=200);

        return JSONResponse(content={'message':'product not found'}, status_code=404);


    def _createProduct(self, product : ProductCreate = Body()) -> JSONResponse:

        prod : Product | None = self._repository.save(product);

        if prod is not None:
            return JSONResponse(content={'message':'product created', 'product':jsonable_encoder(prod)},status_code=201);

        return JSONResponse(content={'message':'product no created'},status_code=400);

    def _deleteProduct(self, id : int) -> JSONResponse:

        prod : Product | None = self._repository.delete(ProductID(productid=id));

        if prod is not None:

            return JSONResponse(content={'message':'produc deleted','product':jsonable_encoder(prod)},status_code=200);

        return JSONResponse(content={'message':'product not deleted'}, status_code=400);



    def _updateProduct(self, id: int, product: ProductCreate = Body()) -> JSONResponse:

        aux : dict[str,Any] = product.model_dump();
        prod : Product | None = self._repository.update(Product(productid=id,**aux));

        if prod is not None:

            return JSONResponse(content={'message':'product updated', 'product':jsonable_encoder(prod)},status_code=200);

        return JSONResponse(content={'message':'product not updated'},status_code=400);

    

    @property
    def router(self) -> APIRouter:
        return self._router;


