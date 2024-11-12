import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "room_id,date_from,date_to,booked_rooms,status_code",
    [
        (4, "2030-05-01", "2030-05-15", 3, 200),
        (4, "2030-05-01", "2030-05-15", 4, 200),
        (4, "2030-05-01", "2030-05-15", 5, 200),
        (4, "2030-05-01", "2030-05-15", 6, 200),
        (4, "2030-05-01", "2030-05-15", 7, 200),
        (4, "2030-05-01", "2030-05-15", 8, 200),
        (4, "2030-05-01", "2030-05-15", 9, 200),
        (4, "2030-05-01", "2030-05-15", 10, 200),
        (4, "2030-05-01", "2030-05-15", 10, 409),
        (4, "2030-05-01", "2030-06-15", 10, 400),
        (4, "2031-05-01", "2030-05-15", 10, 409),
        (3, "abc", "abc", 10, 422),
    ],
)
async def test_add_and_get_booking(
    room_id: int,
    date_from: str,
    date_to: str,
    booked_rooms: int,
    status_code: int,
    authenticated_ac: AsyncClient,
):
    response = await authenticated_ac.post(
        "/bookings",
        params={"room_id": room_id, "date_from": date_from, "date_to": date_to},
    )

    assert response.status_code == status_code

    response = await authenticated_ac.get("/bookings")
    assert len(response.json()) == booked_rooms


@pytest.mark.parametrize(
    "booking_id,booked_rooms,status_code",
    [
        (4, 9, 204),
        (5, 8, 204),
        (6, 7, 204),
        ("...", 7, 422),
    ],
)
async def test_delete_booking(
    booking_id: int, booked_rooms: int, status_code: int, authenticated_ac: AsyncClient
):
    response = await authenticated_ac.delete(
        "/bookings", params={"booking_id": booking_id}
    )
    assert response.status_code == status_code

    response = await authenticated_ac.get("/bookings")
    assert len(response.json()) == booked_rooms
