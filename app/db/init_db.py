import logging
from sqlalchemy.orm import Session

from app import crud, schemas
from app.db import (
    base,
)  # noqa: F401 # import necessary so that all models are pre-initialized
from app.core.config import settings

logger = logging.getLogger(__name__)

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28

FIRST_SUPERUSER = "admin@recipeapi.com"

RECIPES = [
    {
        "id": 0,
        "label": "Chicken",
        "source": "Web",
        "url": "https://google.com",
    },
    {
        "id": 1,
        "label": "Mutton",
        "source": "Web",
        "url": "https://google.com",
    },
    {
        "id": 2,
        "label": "Duck",
        "source": "Web",
        "url": "https://google.com",
    },
    {
        "id": 3,
        "label": "Goose",
        "source": "Web",
        "url": "https://google.com",
    },
]


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)
    if FIRST_SUPERUSER:
        user = crud.user.get_by_email(db, email=FIRST_SUPERUSER)
        if not user:
            user_in = schemas.UserCreate(
                first_name="Initial Super User",
                last_name="Super",
                email=FIRST_SUPERUSER,
                is_superuser=True,
                password=settings.FIRST_SUPERUSER_PW,
            )
            user = crud.user.create(db, obj_in=user_in)  # noqa: F841
        else:
            logger.warning(
                "Skipping creating superuser. User with email "
                f"{FIRST_SUPERUSER} already exists. "
            )
        if not user.recipes:
            for recipe in RECIPES:
                recipe_in = schemas.RecipeCreate(
                    label=recipe["label"],
                    source=recipe["source"],
                    url=recipe["url"],
                    submitter_id=user.id,
                )
                crud.recipe.create(db, obj_in=recipe_in)
    else:
        logger.warning(
            "Skipping creating superuser.  FIRST_SUPERUSER needs to be "
            "provided as an env variable. "
            "e.g.  FIRST_SUPERUSER=admin@api.coursemaker.io"
        )
