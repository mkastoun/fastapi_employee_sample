from fastapi import APIRouter

from app.patients.api import router as patients_router
from app.doctors.api import router as doctors_router

api_router = APIRouter()

include_api = api_router.include_router

routers = (
    (patients_router, "patients", "patients"),
    (doctors_router, "doctors", "doctors"),
)

for router_item in routers:
    router, prefix, tag = router_item

    if tag:
        include_api(router, prefix=f"/{prefix}", tags=[tag])
    else:
        include_api(router, prefix=f"/{prefix}")
