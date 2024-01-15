from typing import Union, Optional
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates

from app.schemas import (
    Recipe,
    RecipeCreate,
    RecipeSearchResults,
    RecipeUpdateRestricted,
)

from app.recipe_data import RECIPES

BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))

app = FastAPI(title="Recipe API")


@app.get("/", status_code=200)
async def root(request: Request) -> dict:
    return TEMPLATES.TemplateResponse(
        name="index.html",
        context={
            "request": request,
            "recipes": RECIPES,
        },
    )


@app.get("/recipes/{recipe_id}", status_code=200)
async def fetch_recipe(*, recipe_id: int) -> dict:
    res = [recipe for recipe in RECIPES if recipe["id"] == recipe_id]
    if not res:
        raise HTTPException(
            status_code=404, detail=f"Recipe with id: {recipe_id} not found"
        )
    return res[0]


@app.get("/search/", status_code=200, response_model=RecipeSearchResults)
async def search_recipes(
    *,
    keyword: Optional[str] = None,
    max_results: Optional[int] = 10,
) -> dict:
    if not keyword:
        return {
            "results": RECIPES[:max_results],
        }

    res = [recipe for recipe in RECIPES if keyword.lower() in recipe["label"].lower()]
    return {
        "results": res,
    }


@app.post("/recipes/", status_code=201, response_model=Recipe)
async def create_recipe(
    *,
    recipe_in: RecipeCreate,
) -> dict:
    new_recipe_id = len(RECIPES)

    new_recipe_entry = Recipe(
        id=new_recipe_id,
        label=recipe_in.label,
        source=recipe_in.source,
        url=recipe_in.url,
    )

    RECIPES.append(new_recipe_entry.model_dump())

    return new_recipe_entry


@app.put("/recipes/", status_code=200, response_model=Recipe)
async def update_recipe(
    *,
    recipe_update: RecipeUpdateRestricted,
) -> dict:
    res = [recipe for recipe in RECIPES if recipe["id"] == recipe_update.id]
    if not res:
        raise HTTPException(
            status_code=404, detail=f"Recipe with id: {recipe_update.id} not found"
        )
    recipe = res[0]
    recipe["label"] = recipe_update.label
    recipe["source"] = recipe_update.source
    recipe["url"] = recipe_update.url

    return recipe


@app.delete("/recipes/{recipe_id}", status_code=200, response_model=Recipe)
async def delete_recipe(
    *,
    recipe_id: int,
) -> dict:
    res = [recipe for recipe in RECIPES if recipe["id"] == recipe_id]
    if not res:
        raise HTTPException(
            status_code=404, detail=f"Recipe with id: {recipe_id} not found"
        )

    recipe = res[0]
    RECIPES.remove(recipe)

    return recipe
