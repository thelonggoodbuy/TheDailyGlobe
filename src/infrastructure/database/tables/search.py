from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer, String
from src.domain.entities.search.search_entities import SearchRequestEntity
from src.infrastructure.database.metadata import mapper_registry


print('=======search tables==============')
print(f"Registry ID in {__name__}: {id(mapper_registry)}")

SearchRequestTable = Table(
    # Table name
    "search_request",
    # Metadata
    mapper_registry.metadata,
    #Unique identifier for search request
    Column("id", Integer, primary_key=True, autoincrement=True),

    # search request`s text
    Column("text", String(length=255), nullable=False),

    # totally quantity of requests
    Column("quantity_of_search_requests", Integer),
    )

# Map the SearchRequest class to the user_table
mapper_registry.map_imperatively(
    SearchRequestEntity,
    SearchRequestTable
)




print("Registered tables in Search module:")
print(mapper_registry.metadata.tables.keys())