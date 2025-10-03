from fastapi import FastAPI

from app.api.cats import router as cats_router
from app.api.missions import router as missions_router
from app.api.targets import router as targets_router

app = FastAPI(title="Spy Cat Agency API", version="1.0.0")

app.include_router(cats_router)
app.include_router(missions_router)
app.include_router(targets_router)


@app.get("/")
def read_root():
    return {"message": "Hello Spy Cat Agency!"}
