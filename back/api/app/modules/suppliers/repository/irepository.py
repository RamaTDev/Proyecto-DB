

from abc import ABC, abstractmethod
from typing import List

from app.modules.suppliers.schemas import Supplier, SupplierCreate, SupplierID, SupplierUpdate


class ISupplierRepository(ABC):


    @abstractmethod
    def findAll(self) -> List[Supplier] | List:
        pass;

    @abstractmethod
    def findById(self, supplierid : SupplierID) -> Supplier | None:
        pass;

    @abstractmethod
    def save(self, supplier : SupplierCreate) -> Supplier | None:
        pass;

    @abstractmethod
    def update(self, supplierid: SupplierID, supplier: SupplierUpdate ) -> Supplier | None:
        pass;

    @abstractmethod
    def delete(self, supplierid: SupplierID) -> Supplier | None:
        pass;

    @abstractmethod
    def activate(self, supplierid: SupplierID) -> Supplier | None:
        pass;




