from typing import Optional
import asyncio
from sqlalchemy.orm import Session
import httpx
from fastapi import APIRouter, HTTPException, Query, Depends

from app.clients.reddit import RedditClient
from app.schemas.recipe import (
    Recipe,
    RecipeBase,
    RecipeCreate,
    RecipeSearchResults,
    RecipeUpdateRestricted,
)
from app import crud
from app.api import deps
from app.models.user import User


RECIPE_SUBREDDITS = ["recipes", "easyrecipes", "TopSecretRecipes"]

router = APIRouter()


@router.get("/{recipe_id}", status_code=200)
async def fetch_recipe(
    *,
    recipe_id: int,
    db: Session = Depends(deps.get_db),
) -> dict:
    result = crud.recipe.get(db=db, id=recipe_id)
    if not result:
        # the exception is raised, not returned - you will get a validation
        # error otherwise.
        raise HTTPException(
            status_code=404, detail=f"Recipe with ID {recipe_id} not found"
        )

    return result


@router.get("/search/", status_code=200, response_model=RecipeSearchResults)
async def search_recipes(
    *,
    keyword: Optional[str] = None,
    max_results: Optional[int] = 10,
    db: Session = Depends(deps.get_db),
) -> dict:
    recipes = crud.recipe.get_multi(db=db, limit=max_results)

    if not keyword:
        return {"results": recipes}

    results = filter(lambda recipe: keyword.lower() in recipe.label.lower(), recipes)
    return {"results": list(results)[:max_results]}


@router.post("/", status_code=201, response_model=Recipe)
async def create_recipe(
    *,
    recipe_in: RecipeBase,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(
        deps.get_current_user
    ),  # allow only if a user is logged-in
) -> dict:
    new_recipe = RecipeCreate(
        label=recipe_in.label,
        source=recipe_in.source,
        url=recipe_in.url,
        submitter_id=current_user.id,
    )
    recipe = crud.recipe.create(db=db, obj_in=new_recipe)

    return recipe


@router.put("/", status_code=200, response_model=Recipe)
async def update_recipe(
    *,
    recipe_update: RecipeUpdateRestricted,
    db: Session = Depends(deps.get_db),
    user: User = Depends(deps.get_current_user),
) -> dict:
    updatable_recipe = crud.recipe.get(
        db=db,
        id=recipe_update.id,
    )

    if not updatable_recipe:
        raise HTTPException(
            status_code=400, detail=f"Recipe with id: {recipe_update.id} not found!"
        )

    if updatable_recipe.submitter_id != user.id:
        raise HTTPException(
            status_code=405,
            detail=f"Recipe with id: {recipe_update.id} doesn't belong to logged in user",
        )

    updated_recipe = crud.recipe.update(
        db=db,
        db_obj=updatable_recipe,
        obj_in=recipe_update,
    )

    return updated_recipe


@router.delete("/{recipe_id}", status_code=200, response_model=Recipe)
async def delete_recipe(
    *,
    recipe_id: int,
    db: Session = Depends(deps.get_db),
    user: User = Depends(deps.get_current_user),
) -> dict:
    recipe = crud.recipe.get(
        db=db,
        id=recipe_id,
    )

    if not recipe:
        raise HTTPException(
            status_code=400, detail=f"Recipe with id: {recipe_id} not found!"
        )

    if recipe.submitter_id != user.id:
        raise HTTPException(
            status_code=405,
            detail=f"Recipe with id: {recipe_id} doesn't belong to logged in user",
        )

    crud.recipe.remove(db=db, id=recipe_id)

    return recipe


@router.get("/ideas/async")
async def fetch_ideas_async(
    reddit_client: RedditClient = Depends(deps.get_reddit_client),
    user: User = Depends(
        deps.get_current_active_superuser
    ),  # allow only if current user is superuser
) -> dict:
    results = await asyncio.gather(
        *[
            reddit_client.get_reddit_top_async(subreddit=subreddit)
            for subreddit in RECIPE_SUBREDDITS
        ]
    )
    return dict(zip(RECIPE_SUBREDDITS, results))
