from fastapi import APIRouter, Body, Query
from sqlalchemy import func, insert, select

from src.api.dependecies import PaginationDep
from src.database import async_session_maker, engine
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel, HotelPATCH


router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(default=None, description="Название отеля"),
    location: str | None = Query(default=None, description="Локация отеля"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        query = select(HotelsOrm)
        if title is not None:
            query = query.filter(func.lower(HotelsOrm.title).like(f"%{title.strip().lower()}%"))
        if location is not None:
            query = query.filter(func.lower(HotelsOrm.location).like(f"%{location.strip().lower()}%"))
        query = (
            query
            .limit(per_page)
            .offset((pagination.page - 1) * per_page)
        )
        result = await session.execute(query)
        hotels = result.scalars().all()

    return hotels


@router.delete(
    path="/{hotel_id}",
    summary="Удалить отель",
    )
def delete_hotel(hotel_id: int):
    return {"status": "OK"}


@router.post("")
async def create_hotel(
    hotel_data: Hotel = Body(openapi_examples={
        "1": {
            "summary": "Бейрут", "value": {
                "title": "Отель Бейрут", "location": "Бейрут, ул. Абу-Даби, 1"
                }},
        "2": {
            "summary": "Братислава", "value": {
                "title": "Шикарный отель",
                "location": "Братислава, ул. Пушкина, 12"
                }
        }
    }),
) -> dict[str, str]:
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        print(add_hotel_stmt.compile(
            engine, compile_kwargs={"literal_binds": True})
        )
        await session.execute(add_hotel_stmt)
        await session.commit()
    return {"status": "OK"}


@router.put("/{hotel_id}")
def update_hotel(
    hotel_id: int,
    hotel_data: Hotel
):
    return {"status": "OK"}


@router.patch("/{hotel_id}")
def partial_update_hotel(
    hotel_id: int,
    hotel_data: HotelPATCH
):
    return {"status": "OK"}
