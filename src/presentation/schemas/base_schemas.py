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
    # model_config = ConfigDict(
    #     alias_generator=to_camel,
    #     populate_by_name=True,
    #     from_attributes=True,
        
    # )



    # model_config = ConfigDict(
    #     alias_generator=lambda field_name: ''.join(
    #         word.capitalize() if i > 0 else word
    #         for i, word in enumerate(field_name.split('_'))
    #     ),
    #     populate_by_name=True,
    #     from_attributes=True,
    # )




class BaseResponseSchema(BaseSchema):
    error: bool = True
    message: Optional[str] = None
    data: Optional[dict]

    