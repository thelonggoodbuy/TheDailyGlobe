from abc import abstractmethod, ABC
from typing import Protocol


class ITokenService(ABC):
    """Check if user is registered in system"""

    @abstractmethod
    async def create_access_token(self):
        pass


class ISearchService(ABC):

    @abstractmethod
    async def full_text_search():
        pass