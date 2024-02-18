from fastapi import APIRouter

router = APIRouter()


@router.get("/Lottery")
async def lottery():
    return {"message": "Welcome To Lottery"}
