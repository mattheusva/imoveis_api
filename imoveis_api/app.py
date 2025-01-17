from http import HTTPStatus

from fastapi import FastAPI

from imoveis_api.routers import properties, users
from imoveis_api.schemas import Message

app = FastAPI()

app.include_router(users.router)
app.include_router(properties.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Olá, mundo!'}
