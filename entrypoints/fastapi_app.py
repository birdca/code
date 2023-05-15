from fastapi import FastAPI, HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
from adapters.orm import start_mappers
from adapters.repository import SqlAlchemyRepository
from domain.model import OrderLine, OutOfStock
from service_layer.services import allocate, InvalidSku


start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_sqlite_uri()))
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/allocate")
async def allocate_endpoint(line: OrderLine):
    session = get_session()
    repo = SqlAlchemyRepository(session)
    try:
        batchref = allocate(line, repo, session)
    except (OutOfStock, InvalidSku) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    session.commit()

    return {"batchref": batchref}
