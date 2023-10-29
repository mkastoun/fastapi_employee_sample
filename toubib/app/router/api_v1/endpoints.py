from fastapi import APIRouter

from toubib.app.patients.api import router as patients_router

api_router = APIRouter()

include_api = api_router.include_router

routers = (
    (patients_router, "patients", "patients"),
)

for router_item in routers:
    router, prefix, tag = router_item

    if tag:
        include_api(router, prefix=f"/{prefix}", tags=[tag])
    else:
        include_api(router, prefix=f"/{prefix}")
