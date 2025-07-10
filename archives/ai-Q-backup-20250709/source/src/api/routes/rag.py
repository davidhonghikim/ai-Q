from fastapi import APIRouter, Depends
import httpx
from config.settings import get_settings

router = APIRouter()

@router.get("/")
async def get_rag(settings=Depends(get_settings)):
    url = settings.external_api.placeholder_base_url + settings.external_api.rag_endpoint
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        data = resp.json()
    return {
        "agent": settings.external_api.agent_name,
        "version": settings.external_api.agent_version,
        "data": data
    } 