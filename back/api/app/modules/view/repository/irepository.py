

from abc import ABC,abstractmethod
from typing import List

from app.modules.view.schema import View, ViewFilter


class IViewRepository(ABC):

    @abstractmethod
    def filter(self, viewFilter : ViewFilter ) -> List[View]:
        pass;


