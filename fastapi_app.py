from fastapi import FastAPI, HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
import model
import orm
import repository


orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_sqlite_uri()))
app = FastAPI()


def is_valid_sku(sku, batches):
    for batch in batches:
        if batch.sku == sku:
            return True
    return False


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/allocate")
async def allocate_endpoint(line: model.OrderLine):
    session = get_session()
    batches = repository.SqlAlchemyRepository(session).list()

    if not is_valid_sku(line.sku, batches):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"SKU {line.sku} not found")

    try:
        batchref = model.allocation(line, batches)
    except model.OutOfStock as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    session.commit()

    return {'batchref': batchref}
