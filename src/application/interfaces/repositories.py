from litestar.contrib.sqlalchemy.repository import SQLAlchemyAsyncRepository
from sqlalchemy.ext.asyncio import AsyncSession


# TODO generic repository/
class IAlchemyRepository(SQLAlchemyAsyncRepository):
    """Base repository class."""

    _session: AsyncSession

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        """Configure the repository object."""
        self._session: AsyncSession = session
