from sqlalchemy import MetaData
from sqlalchemy.orm import registry


# print('=============creating and init metadata======================')
metadata = MetaData()
mapper_registry = registry(metadata=metadata)
