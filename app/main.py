import uvicorn
from fastapi import FastAPI
from starlette.responses import JSONResponse

from app.cache import clean_cache
from app.router import router

# from app.db import (
#     clean_tables, delete_tables, create_tables
# )


app = FastAPI(
    title="Restaurant menu service",
    version="1.0.0",
    docs_url="/api/openapi",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

app.include_router(router=router, prefix='/api/v1/menus')


# @app.on_event("startup")
# def startup():
#     create_tables()


@app.on_event("shutdown")
def on_shutdown():
    clean_cache()
    # delete_tables()


@app.get("/")
def homepage():
    return JSONResponse({'message': 'This is a restaurant menu system'})


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="0.0.0.0")
