from typing import Union, Optional
from fastapi import FastAPI

from app.schemas import Recipe, RecipeCreate, RecipeSearchResults

app = FastAPI(title="Recipe API")


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


@app.get("/", status_code=200)
async def root() -> dict:
    return {"msg": "See recipes here"}


@app.get("/recipes/{recipe_id}", status_code=200)
async def fetch_recipe(*, recipe_id: int) -> dict:
    res = [recipe for recipe in RECIPES if recipe["id"] == recipe_id]
    if res:
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


@app.put("/recipes/{recipe_id}", status_code=200)
async def update_recipe(
    *,
    recipe_id: int,
    recipe_in: RecipeCreate,
) -> dict:
    res = [recipe for recipe in RECIPES if recipe["id"] == recipe_id]
    if res:
        recipe = res[0]
        recipe["label"] = recipe_in.label
        recipe["source"] = recipe_in.source
        recipe["url"] = recipe_in.url

        return Recipe.model_validate(recipe)
    return {"msg": "Recipe not found"}


@app.delete("/recipes/{recipe_id}", status_code=200)
async def delete_recipe(
    *,
    recipe_id: int,
) -> dict:
    res = [recipe for recipe in RECIPES if recipe["id"] == recipe_id]
    if res:
        recipe = res[0]
        RECIPES.remove(recipe)

        return {"msg": "Deleted!"}
    return {"msg": "Recipe not found"}
