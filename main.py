from typing import Union
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"msg": "hello world"}


@app.get("/items/{item_id}")
async def read_items(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
