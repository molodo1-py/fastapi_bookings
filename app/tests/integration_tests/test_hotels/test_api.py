import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "location,date_from,date_to,status_code",
    [
        ("Алтай", "2024-11-20", "2024-12-01", 200),
        ("Алтай", "2024-11-20", "2024-12-01", 200),
        ("Коми", "2024-11-20", "2024-12-01", 200),
        ("Алтай", "2025-01-05", "2025-02-20", 400),
        ("Коми", "2025-01-05", "2025-02-20", 400),
        ("Сириус", "2025-01-05", "2025-02-20", 400),
        ("Сириус", "...", "abc", 422),
    ],
)
async def test_get_hotels(
    location: str, date_from: str, date_to: str, status_code: int, ac: AsyncClient
):

    response = await ac.get(
        f"/hotels/{location}", params={"date_from": date_from, "date_to": date_to}
    )

    assert response.status_code == status_code
    
    if status_code == 200:
        for hotel in response.json():
            assert location in hotel.get("location")