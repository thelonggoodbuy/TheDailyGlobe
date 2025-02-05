from dataclasses import dataclass
from src.domain.common.entity import Entity



@dataclass
class NotificationCredentialEntity(Entity):
    """Article model."""
    registraion_token: str
    user_id: int
    is_active: bool
    

