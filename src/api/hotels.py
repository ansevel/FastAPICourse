from fastapi import APIRouter, Body, Query

from src.api.dependecies import PaginationDep
from src.database import async_session_maker
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import HotelAdd, HotelPATCH


router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(default=None, description="Название отеля"),
    location: str | None = Query(default=None, description="Локация отеля"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=(pagination.page - 1) * per_page
        )


@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_one_or_none(id=hotel_id)


@router.delete(
    path="/{hotel_id}",
    summary="Удалить отель",
    )
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.post("")
async def create_hotel(
    hotel_data: HotelAdd = Body(openapi_examples={
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
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def update_hotel(
    hotel_id: int,
    hotel_data: HotelAdd
):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}")
async def partially_update_hotel(
    hotel_id: int,
    hotel_data: HotelPATCH
):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(
            hotel_data, exclude_unset=True, id=hotel_id)
        await session.commit()
    return {"status": "OK"}
