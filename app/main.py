from contextlib import asynccontextmanager
from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Annotated


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Start Event - 
    Load DB - check data present then load json then database

    Stop Event -
    Save new DB to json and then del database intance
    """
    db = ""
    yield
    del db

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"Hello": f"World"}