from pydantic import BaseModel, ConfigDict, AliasGenerator
from pydantic.alias_generators import to_camel, to_snake
from typing import Any, Dict, Optional
from typing import Type





class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_snake,
            serialization_alias=to_camel,
        ),
        populate_by_name=True,
        from_attributes=True,
        
    )


class BaseResponseSchema(BaseSchema):
    """
    Base response schema.
    Args:
        - error (bool)
        - message (str)
        - data (Optional[dict])
    """
    error: bool = True
    message: Optional[str] = None
    data: Optional[dict]

    