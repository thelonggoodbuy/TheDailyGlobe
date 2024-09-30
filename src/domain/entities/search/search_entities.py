from dataclasses import dataclass
from src.domain.common.entity import Entity

from advanced_alchemy.types import DateTimeUTC




# entity for search request
@dataclass
class SearchRequestEntity(Entity):
    """Search request model"""
    text: str
    quantity_of_search_requests: int