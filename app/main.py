from fastapi import FastAPI

from app.api.cats import router as cats_router

app = FastAPI(title="Spy Cat Agency API", version="1.0.0")

app.include_router(cats_router)


@app.get("/")
def read_root():
    return {"message": "Hello Spy Cat Agency!"}
