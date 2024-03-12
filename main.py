from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


db = []

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.get("/hello/")
async def root():
    return {"message": "Hello World!!!"}


@app.get("/hello/{name}/")
async def name(name: str, times: int = 1):
    return {"message": f"Hello {name*times}!!!"}

@app.get("/items/")
async def get_item() -> list[Item]:
    return db

@app.post("/items/")
async def create_item(item: Item) -> bool:
    db.append(item)
    return True
