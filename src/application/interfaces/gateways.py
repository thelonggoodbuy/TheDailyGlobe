from abc import abstractmethod, ABC
from typing import Protocol


class IWriteFileStorageGateway(ABC):
    """Interface for gateways which save files"""

    @abstractmethod
    async def safe_file_in_storage(self):
        pass