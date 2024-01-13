from typing import Union
from fastapi import FastAPI

app = FastAPI(title="Recipe API")


RECIPES = [
    {
        "id": 0,
        "dish": "Chicken",
        "source": "Web",
        "url": "www.google.com",
    },
    {
        "id": 2,
        "dish": "Mutton",
        "source": "Web",
        "url": "www.google.com",
    },
    {
        "id": 3,
        "dish": "Duck",
        "source": "Web",
        "url": "www.google.com",
    },
    {
        "id": 4,
        "dish": "Goose",
        "source": "Web",
        "url": "www.google.com",
    },
]


@app.get("/", status_code=200)
async def read_root():
    return {"msg": "See recipes here"}


@app.get("/recipes/{recipe_id}", status_code=200)
async def fetch_recipe(recipe_id: int):
    res = [recipe for recipe in RECIPES if recipe["id"] == recipe_id]
    if res:
        return res[0]
