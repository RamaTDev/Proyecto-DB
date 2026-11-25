


from fastapi import APIRouter, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.modules.view.repository.irepository import IViewRepository
from app.modules.view.schema import ViewFilter


class ViewRouter():


    _router : APIRouter;
    _repository: IViewRepository;


    def __init__(self, repository: IViewRepository) -> None:
        self._repository = repository;
        self._router = APIRouter(tags=['views']);
        self._registerRoutes();

    def _registerRoutes(self) -> None:
        self._router.add_api_route('/',self._filterView,methods=['GET']);


    def _filterView(self, filter : ViewFilter = Query()) -> JSONResponse:

        res = self._repository.filter(filter);

        return JSONResponse(content={'filter':jsonable_encoder(res)});
        


    @property
    def router(self) -> APIRouter:
        return self._router;
        

    