from fastapi import APIRouter
from routers.authentication.views import app as authentication_app
from routers.ingestion.views import app as ingestion_app
from routers.qa.views import app as qa_app
from routers.retrieval.views import app as retrieval_app

routes = APIRouter()

routes.include_router(
    authentication_app,
    tags=["authentication"],
    prefix="/v1",
)
routes.include_router(
    ingestion_app,
    tags=["ingestion"],
    prefix="/v1",
)
routes.include_router(
    qa_app,
    tags=["qa"],
    prefix="/v1",
)
routes.include_router(
    retrieval_app,
    tags=["retrieval"],
    prefix="/v1",
)


