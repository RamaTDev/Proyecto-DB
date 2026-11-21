

from abc import ABC,abstractmethod
from typing import List

from app.modules.view.schema import View, ProductName, CategoryName, Stock, StockRange


class IViewRepository(ABC):

    @abstractmethod
    def filterByProductName(self, productName: ProductName) -> List[View]:
        pass;


    @abstractmethod
    def filterByCategoryName(self, categoryName: CategoryName) -> List[View]: 
        pass;


    @abstractmethod
    def graterThanStock(self,  stock : Stock) -> List[View]:
        pass;

    @abstractmethod
    def lessThanStock(self,  stock: Stock) -> List[View]:
        pass;


    @abstractmethod
    def rangeStock(self,  stock: StockRange) -> List[View]:
        pass;
