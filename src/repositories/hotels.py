from sqlalchemy import func, insert, select

from src.database import engine
from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm


class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(
            self,
            location,
            title,
            limit,
            offset,
    ):
        query = select(HotelsOrm)
        if title is not None:
            query = query.filter(
                func.lower(HotelsOrm.title)
                .contains(title.strip().lower())
            )
        if location is not None:
            query = query.filter(
                func.lower(HotelsOrm.location)
                .contains(location.strip().lower())
            )
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        print(query.compile(
            engine, compile_kwargs={"literal_binds": True})
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def add(self, data):
        stmt = (
            insert(self.model)
            .values(**data.model_dump())
            .returning(self.model)
        )
        hotel = await self.session.execute(stmt)
        return hotel.scalars().first()