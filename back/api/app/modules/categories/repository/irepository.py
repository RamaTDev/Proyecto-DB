

from abc import ABC, abstractmethod
from typing import List

from app.modules.categories.schemas import Category, CategoryCreate, CategoryID


class ICategoryRepository(ABC):


    @abstractmethod
    def findAll(self) -> List[Category]:
        pass;
    
    @abstractmethod
    def findById(self, category : CategoryID) -> Category | None:
        pass;
    
    @abstractmethod
    def save(self, category : CategoryCreate) -> str | None:
        pass;
    
    @abstractmethod
    def update(self, categoryid: CategoryID, category: CategoryCreate ) -> str | None:
        pass;
    
    @abstractmethod
    def delete(self, categoryid: CategoryID) -> str | None:
        pass;
    
    @abstractmethod
    def activate(self, categoryid: CategoryID) -> str | None:
        pass;
    