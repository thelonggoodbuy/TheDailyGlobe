"""Get the SQLAlchemy engine instance."""

from typing import Any
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine

from src.main.config.settings import DatabaseSettings
from sqlalchemy.orm import registry





def get_alchemy_engine(db_settings: DatabaseSettings) -> AsyncEngine:
    """Get the SQLAlchemy engine instance."""
    # prepare the engine
    engine = create_async_engine(
        url=db_settings.URL,
    )

    return engine







# def get_alchemy_config(
#     engine: AsyncEngine,
#     db_settings: DatabaseSettings,
# ) -> SQLAlchemyAsyncConfig:
#     """Get SQLAlchemy configuration."""
#     return SQLAlchemyAsyncConfig(
#         engine_instance=engine,
#         before_send_handler=async_autocommit_before_send_handler,
#         session_config=AsyncSessionConfig(expire_on_commit=False),
#         alembic_config=AlembicAsyncConfig(
#             version_table_name=db_settings.MIGRATION_DDL_VERSION_TABLE,
#             script_config=db_settings.MIGRATION_CONFIG,
#             script_location=db_settings.MIGRATION_PATH,
#         ),
#     )
