





from sqlalchemy import select
from src.application.interfaces.repositories import BaseTariffRepository, IAlchemyRepository
from src.domain.entities.tariffs.tariffs_entities import TariffEntity
from src.presentation.schemas.subscriptions import AllTariffResponseSchema


class TariffRepository(BaseTariffRepository, IAlchemyRepository):

    async def return_all(self) -> AllTariffResponseSchema | None:
        query = select(TariffEntity).filter()
        tariffs_rows = await self._session.execute(query)
        result = tariffs_rows.scalars().all()
        print('---result---')
        print(result)
        print('-----------')
        return result
    

    async def return_tariff_by_id(self, tariff_id) -> AllTariffResponseSchema | None:
        query = select(TariffEntity).filter(TariffEntity.id == tariff_id)
        tariffs_row = await self._session.execute(query)
        result = tariffs_row.scalar_one_or_none()
        return result