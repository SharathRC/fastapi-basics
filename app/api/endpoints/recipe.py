from typing import Optional
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Query, Depends

from app.schemas.recipe import (
    Recipe,
    RecipeCreate,
    RecipeSearchResults,
)
from app import crud
from app.api import deps

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
    recipe_in: RecipeCreate,
    db: Session = Depends(deps.get_db),
) -> dict:
    recipe = crud.recipe.create(db=db, obj_in=recipe_in)

    return recipe


# @router.put("/", status_code=200, response_model=Recipe)
# async def update_recipe(
#     *,
#     recipe_update: RecipeUpdateRestricted,
#     db: Session = Depends(deps.get_db),
# ) -> dict:
#     res = [recipe for recipe in RECIPES if recipe["id"] == recipe_update.id]
#     if not res:
#         raise HTTPException(
#             status_code=404, detail=f"Recipe with id: {recipe_update.id} not found"
#         )
#     recipe = res[0]
#     recipe["label"] = recipe_update.label
#     recipe["source"] = recipe_update.source
#     recipe["url"] = recipe_update.url

#     return recipe


# @router.delete("/{recipe_id}", status_code=200, response_model=Recipe)
# async def delete_recipe(
#     *,
#     recipe_id: int,
#     db: Session = Depends(deps.get_db),
# ) -> dict:
#     res = [recipe for recipe in RECIPES if recipe["id"] == recipe_id]
#     if not res:
#         raise HTTPException(
#             status_code=404, detail=f"Recipe with id: {recipe_id} not found"
#         )

#     recipe = res[0]
#     RECIPES.remove(recipe)

#     return recipe
