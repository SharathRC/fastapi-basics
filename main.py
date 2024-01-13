from typing import Union, Optional
from fastapi import FastAPI

app = FastAPI(title="Recipe API")


RECIPES = [
    {
        "id": 0,
        "label": "Chicken",
        "source": "Web",
        "url": "www.google.com",
    },
    {
        "id": 2,
        "label": "Mutton",
        "source": "Web",
        "url": "www.google.com",
    },
    {
        "id": 3,
        "label": "Duck",
        "source": "Web",
        "url": "www.google.com",
    },
    {
        "id": 4,
        "label": "Goose",
        "source": "Web",
        "url": "www.google.com",
    },
]


@app.get("/", status_code=200)
async def read_root() -> dict:
    return {"msg": "See recipes here"}


@app.get("/recipes/{recipe_id}", status_code=200)
async def fetch_recipe(recipe_id: int) -> dict:
    res = [recipe for recipe in RECIPES if recipe["id"] == recipe_id]
    if res:
        return res[0]


@app.get("/search/", status_code=200)
async def search_recipes(
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
