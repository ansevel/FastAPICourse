from fastapi import APIRouter, Body, Query

from schemas.hotels import Hotel, HotelPATCH

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spd"},
]

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
def get_hotels(
    id: int | None = Query(default=None, description="ID отеля"),
    title: str | None = Query(default=None, description="Название отеля"),
    page: int | None = Query(1, description="Номер страницы", ge=1),
    per_page: int | None = Query(10, description="Количество отелей на странице", ge=1),
):
    hotels_ = []
    start = (page - 1) * per_page
    end = page * per_page
    for counter, hotel in enumerate(hotels):
        if id is not None and hotel["id"] != id:
            continue
        if title is not None and hotel["title"] != title:
            continue
        if counter >= start and counter < end:
            hotels_.append(hotel)

    return hotels_


@router.delete(
    path="/{hotel_id}",
    summary="Удалить отель",
    )
def delete_hotel(hotel_id: int):
    for i, hotel in enumerate(hotels):
        if hotel["id"] == hotel_id:
            del hotels[i]
            break
    return {"status": "OK"}


@router.post("")
def create_hotel(
    hotel_data: Hotel = Body(openapi_examples={
        "1": {
            "summary": "Бейрут", "value": {
                "title": "Бейрут отель", "name": "beirut"
                }},
        "2": {
            "summary": "Братислава", "value": {
                "title": "Братислава отель", "name": "bratislava"
                }
        }
    }),
) -> dict[str, str]:
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name
    })
    return {"status": "OK"}


@router.put("/{hotel_id}")
def update_hotel(
    hotel_id: int,
    hotel_data: Hotel
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = hotel_data.title
            hotel["name"] = hotel_data.name
            break
    return {"status": "OK"}


@router.patch("/{hotel_id}")
def partial_update_hotel(
    hotel_id: int,
    hotel_data: HotelPATCH
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if hotel_data.title is not None:
                hotel["title"] = hotel_data.title
            if hotel_data.name is not None:
                hotel["name"] = hotel_data.name
            break
    return {"status": "OK"}
