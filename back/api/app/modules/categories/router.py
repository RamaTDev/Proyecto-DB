

from typing import List

from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.modules.categories.repository.irepository import ICategoryRepository
from app.modules.categories.schemas import Category, CategoryCreate, CategoryID


class CategoryRouter():

    _repository : ICategoryRepository;
    _router : APIRouter; 


    def __init__(self, repository : ICategoryRepository) -> None:
        self._repository = repository;
        self._router = APIRouter(tags=['categories']);
        self._registerRoutes();


    def _registerRoutes(self) -> None:
        self._router.add_api_route('/',self._getCategories,methods=['GET']);
        self._router.add_api_route('/',self._createCategory, methods=['POST']);
        self._router.add_api_route('/{id}',self._getCategoryById,methods=['GET']);
        self._router.add_api_route('/{id}',self._deleteCategory,methods=['DELETE']);
        self.router.add_api_route('/{id}',self._updateCategory,methods=['PUT']);
        self.router.add_api_route('/{id}',self._activateCategory,methods=['POST']);
    



    def _getCategories(self) -> JSONResponse:

        res : List[Category] = self._repository.findAll();

        return JSONResponse(content={'categories':jsonable_encoder(res)}, status_code=200);


    def _getCategoryById(self, id : int) -> JSONResponse:

        cat : Category | None = self._repository.findById(CategoryID(categoryid=id));

        if cat is not None:

            return JSONResponse(content={'category':jsonable_encoder(cat)},status_code=200);

        return JSONResponse(content={'error':{}});


    def _createCategory(self, category: CategoryCreate = Body()) -> JSONResponse:

        res : str | None = self._repository.save(category);

        if res is not None:
            return JSONResponse(content={'message':res},status_code=201);

        return JSONResponse(content={'message':'an error ocurred.'}, status_code=400);


    def _updateCategory(self, id: int, category: CategoryCreate = Body()) -> JSONResponse:

        res : str | None = self._repository.update(CategoryID(categoryid=id),category);

        if res is not None:
            return JSONResponse(content={'message':res},status_code=200);

        return JSONResponse(content={'message':'an error ocurred.'}, status_code=400);


    def _deleteCategory(self, id:int) -> JSONResponse:

        res : str | None = self._repository.delete(CategoryID(categoryid=id));

        if res is not None:
            return JSONResponse(content={'message':res},status_code=200);

        return JSONResponse(content={'message':'an error ocurred.'}, status_code=400);


    def _activateCategory(self, id:int) -> JSONResponse:

        res : str | None = self._repository.activate(CategoryID(categoryid=id));

        if res is not None:
            return JSONResponse(content={'message':res},status_code=200);

        return JSONResponse(content={'message':'an error ocurred.'}, status_code=400);

    @property
    def router(self) -> APIRouter:
        return self._router;



        