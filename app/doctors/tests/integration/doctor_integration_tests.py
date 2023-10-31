from httpx import AsyncClient
from sqlalchemy import insert, select
from sqlmodel import Session

from app.doctors.models import Doctor


async def test_create_doctor(
        client: AsyncClient,
        session: Session,
        test_data: dict
):
    """
    Test should create successfully a doctor and check it values
    Args:
        client:
        session:
        test_data:

    Returns:

    """
    payload = test_data["case_create"]["payload"]
    response = await client.post("/doctors", json=payload)

    assert response.status_code == 201

    got = response.json()
    want = test_data["case_create"]["want"]

    for k, v in want.items():
        assert got["data"][k] == v

    statement = select(Doctor).where(Doctor.id == got["data"]["id"])
    result = session.execute(statement=statement)
    doctor = result.scalar_one()

    for k, v in want.items():
        if k == 'hiring_date':
            hiring_date = getattr(doctor, k).strftime("%Y-%m-%d")
            assert hiring_date == v
        else:
            assert getattr(doctor, k) == v
