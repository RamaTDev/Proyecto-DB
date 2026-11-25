
from abc import ABC, abstractmethod
from typing import List

from app.modules.products.schemas import Product, ProductID, ProductCreate, ProductUpdate


class IProductRepository(ABC):

    @abstractmethod
    def findAll(self) -> List[Product]:
        pass;  

    @abstractmethod
    def findById(self, product: ProductID) -> Product | None:
        pass;

    @abstractmethod
    def save(self, product : ProductCreate) -> Product | None:
        pass;

    @abstractmethod
    def delete(self, product : ProductID) -> Product | None:
        pass;

    @abstractmethod
    def update(self, productid: ProductID,  product : ProductUpdate) -> Product | None:
        pass;

    @abstractmethod
    def activate(self, productid: ProductID) -> Product | None:
        pass;

    