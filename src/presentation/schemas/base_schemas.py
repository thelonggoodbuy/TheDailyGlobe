from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from typing import Any, Dict, Optional
from typing import Type





class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )



class BaseResponseSchema(BaseModel):
    error: bool = True
    message: Optional[str] = None
    data: Optional[dict]