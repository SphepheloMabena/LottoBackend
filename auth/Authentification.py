from fastapi import APIRouter

router = APIRouter()


@router.get("/Auth")
async def auth():
    return {"message": "Welcome To Lottery"}
