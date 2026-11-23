

from typing import List

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.modules.suppliers.repository.irepository import ISupplierRepository
from app.modules.suppliers.schemas import Supplier, SupplierCreate, SupplierID, SupplierUpdate


class SupplierRouter():

    _router : APIRouter;
    _repository : ISupplierRepository;


    def __init__(self, repository : ISupplierRepository) -> None:
        self._repository = repository;
        self._router = APIRouter(tags=['suppliers']);
        self._registerRoutes();


    def _registerRoutes(self) -> None:
        self._router.add_api_route('/',self._getSuppliers, methods=['GET']);
        self._router.add_api_route('/{id}',self._getSupplierById, methods=['GET']);
        self._router.add_api_route('/',self._createSupplier,methods=['POST']);
        self._router.add_api_route('/{id}',self._updateSupplier,methods=['PUT']);
        self.router.add_api_route('/{id}',self._deleteSupplier,methods=['DELETE']);
        self.router.add_api_route('/{id}/activate',self._activateSupplier,methods=['POST']);


    def _getSuppliers(self) -> JSONResponse:
        res : List[Supplier] = [];
        res = self._repository.findAll();
        return JSONResponse(content={'suppliers':jsonable_encoder(res)});


    def _getSupplierById(self, id : int) -> JSONResponse:

        res : Supplier | None = self._repository.findById(SupplierID(supplierid=id));

        if res is not None:
            return JSONResponse(content={'supplier':jsonable_encoder(res)},status_code=200);

        return JSONResponse(content={'message':'not found'}, status_code=404);


    def _createSupplier(self, supplier: SupplierCreate) -> JSONResponse:

        res : Supplier | None = self._repository.save(supplier);

        if res is not None:
            return JSONResponse(content={'supplier':jsonable_encoder(res)}, status_code=200);

        return JSONResponse(content={'error':{}}, status_code=400);


    def _updateSupplier(self, id: int, supplier: SupplierUpdate) -> JSONResponse:

        res : Supplier | None = self._repository.update(SupplierID(supplierid=id),supplier);

        if res is not None:
            return JSONResponse(content={'supplier':jsonable_encoder(res)},status_code=200);

        return JSONResponse(content={'error':{}});


    def _deleteSupplier(self, id:int) -> JSONResponse:

        res : Supplier | None = self._repository.delete(SupplierID(supplierid=id));


        if res is not None:
            return JSONResponse(content={'supplier':jsonable_encoder(res)},status_code=200);


        return JSONResponse(content={'error':{}}, status_code=400);


    def _activateSupplier(self, id: int) -> JSONResponse:

        res : Supplier | None = self._repository.activate(SupplierID(supplierid=id));
        
        
        if res is not None:
            return JSONResponse(content={'supplier':jsonable_encoder(res)},status_code=200);
        
        
        return JSONResponse(content={'error':{}}, status_code=400);
        

        

    @property
    def router(self) -> APIRouter:
        return self._router;





        