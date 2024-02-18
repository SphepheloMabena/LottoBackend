from fastapi import FastAPI, status
from auth.Authentification import router
from lottery import Lottery

app = FastAPI()
app.include_router(router)
app.include_router(Lottery.router)
