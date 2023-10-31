from httpx import AsyncClient
from sqlalchemy import insert, select
from sqlmodel import Session

from app.patients.models import Patient


async def test_create_patient(
        client: AsyncClient,
        session: Session,
        test_data: dict
):
    """
    Test should create successfully a patient and check it values
    Args:
        client:
        session:
        test_data:

    Returns:

    """
    payload = test_data["case_create"]["payload"]
    response = await client.post("/patients", json=payload)

    assert response.status_code == 201

    got = response.json()
    want = test_data["case_create"]["want"]

    for k, v in want.items():
        assert got["data"][k] == v

    statement = select(Patient).where(Patient.id == got["data"]["id"])
    result = session.execute(statement=statement)
    patient = result.scalar_one()

    for k, v in want.items():
        if k == 'date_of_birth':
            dob = getattr(patient, k).strftime("%Y-%m-%d")
            assert dob == v
        else:
            assert getattr(patient, k) == v


async def test_create_patient_with_invalid_email(
        client: AsyncClient,
        session: Session,
        test_data: dict
):
    """
    Test should throw http exception with status 404 exception due to invalid email
    Args:
        client:
        session:
        test_data:

    Returns:

    """
    payload = test_data["case_create_invalid_email"]["payload"]

    response = await client.post("/patients", json=payload)

    assert response.status_code == 422


async def test_create_patient_with_future_dob(
        client: AsyncClient,
        session: Session,
        test_data: dict
):
    """
    Test should throw http exception with status code 422 de to future date of birth
    Args:
        client:
        session:
        test_data:

    Returns:

    """
    payload = test_data["case_create_invalid_email"]["payload"]

    response = await client.post("/patients", json=payload)

    assert response.status_code == 422


async def test_create_patient_with_existing_email(
        client: AsyncClient,
        session: Session,
        test_data: dict
):
    """
    Test should throw http exception conflict with http status 409 due to already existing email
    Args:
        client:
        session:
        test_data:

    Returns:

    """
    payload = test_data["case_create"]["payload"]

    await client.post("/patients", json=payload)
    response = await client.post("/patients", json=payload)

    assert response.status_code == 409


async def test_get_patient(
        client: AsyncClient,
        session: Session,
        test_data: dict
):
    """
    Test should return success on getting patient
    Args:
        client:
        session:
        test_data:

    Returns:

    """
    patient_data = test_data["initial_data"]["patient"]
    statement = insert(Patient).values(patient_data)
    session.execute(statement=statement)
    session.commit()

    response = await client.get(f"patients/{patient_data['id']}")

    assert response.status_code == 200

    got = response.json()
    want = test_data["case_get"]["want"]

    for k, v in want.items():
        assert got["data"][k] == v


async def test_get_not_created_patient(
        client: AsyncClient,
        session: Session,
        test_data: dict
):
    """
    Test should throw http exception with http status 404 due to not found patient
    Args:
        client:
        session:
        test_data:

    Returns:

    """
    response = await client.get(f"patients/1")
    assert response.status_code == 404
