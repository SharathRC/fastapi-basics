from pathlib import Path
from sqlalchemy.orm import Session
from fastapi import FastAPI, APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from app import crud
from app.api import api_router, deps


BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))

root_router = APIRouter()
app = FastAPI(title="Recipe API")


@root_router.get("/", status_code=200)
async def root(
    request: Request,
    db: Session = Depends(deps.get_db),
) -> dict:
    recipes = crud.recipe.get_multi(db=db, limit=10)
    return TEMPLATES.TemplateResponse(
        name="index.html",
        context={
            "request": request,
            "recipes": recipes,
        },
    )


app.include_router(root_router)
app.include_router(api_router, prefix="/api")
