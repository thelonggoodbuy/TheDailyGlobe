""""""
import asyncio
from typing import cast

from sqlalchemy import Column, pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from advanced_alchemy.base import orm_registry


from alembic import context
from alembic.autogenerate import rewriter
from alembic.operations import ops
from sqlalchemy.engine import Connection
from advanced_alchemy.alembic.commands import AlembicCommandConfig
from alembic.runtime.environment import EnvironmentContext
from sqlalchemy.ext.asyncio import create_async_engine


import pprint


from src.infrastructure.database.metadata import metadata


import os
from dotenv import load_dotenv
from sqlalchemy.engine.url import URL

config: AlembicCommandConfig = context.config  # noqa




# Загружаем переменные окружения из .env
load_dotenv()

# config.set_main_option(
#     'sqlalchemy.url',
#     str(URL.create(
#         drivername="postgresql+asyncpg",
#         username=os.getenv("POSTGRES_USER"),
#         password=os.getenv("POSTGRES_PASSWORD"),
#         host=os.getenv("POSTGRES_HOST"),
#         port=os.getenv("POSTGRES_PORT"),
#         database=os.getenv("POSTGRES_DB")
#     ))
# )





# for key, value in config.get_section(config.config_ini_section).items():
#     print('Context value:')
#     print(f"{key}: {value}")


target_metadata=metadata



# print("---> Registered Tables in Metadata <---")
# pprint.pprint(target_metadata.tables.keys())
# print("====config=====")
# print(config)
# print('===============')



writer = rewriter.Rewriter()

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.
    """
    context.configure(
        url=config.db_url,
        target_metadata=target_metadata,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Run migrations."""

    # print(f"Registered tables: {target_metadata.tables.keys()}")

    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine and associate a
    connection with the context.
    """
    configuration = config.get_section(config.config_ini_section) or {}

    # TODO если заработает - убрать колхоз со ссылкой
    
    # configuration["sqlalchemy.url"] = config.db_url
    configuration["sqlalchemy.url"] = config.get_main_option("sqlalchemy.url")

    engine = create_async_engine(url=configuration["sqlalchemy.url"])

    connectable = cast(
        "AsyncEngine",
        # config.engine
        engine
        or async_engine_from_config(
            configuration,
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True,
        ),
    )
    if connectable is None:
        msg = "Could not get engine from config.  Please ensure your `alembic.ini` according to the official Alembic documentation."
        raise RuntimeError(
            msg,
        )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())


# print('===================================================================')

# print('MIGRATION SCIPT FINISHED!!!!!!!!!!!!')

# print('===================================================================')