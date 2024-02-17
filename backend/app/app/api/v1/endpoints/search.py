from fastapi import APIRouter

from app.utils.typesense_func import client

router = APIRouter()

@router.get("")
def search(q:str):
    return q
