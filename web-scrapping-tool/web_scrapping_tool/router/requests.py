from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel

from ..dependencies import get_request_service, get_scrap_service
from ..router.model.scrap import Scrap
from ..services.requests import RequestService
from ..services.scraps import ScrapService
from ..utils.authentication import verify_token
from .model.request import Request, RequestCreate

router = APIRouter(prefix="/requests")

@router.post("", response_model=Request)
async def create_request(request: RequestCreate, service: RequestService = Depends(get_request_service), credentials: HTTPAuthorizationCredentials = Depends(verify_token)):
    db_request = await service.create_request(request_data=request)
    return db_request

@router.get("/{request_id}", response_model=Request)
async def get_request(request_id: str, service: RequestService = Depends(get_request_service)):
    db_request = await service.get_request(request_id=request_id)
    if db_request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    return db_request

@router.get("", response_model=List[Request])
async def get_all_requests(service: RequestService = Depends(get_request_service)):
    return await service.get_all_requests()

@router.put("/{request_id}", response_model=Request)
async def update_request(request_id: str, request: RequestCreate, service: RequestService = Depends(get_request_service), credentials: HTTPAuthorizationCredentials = Depends(verify_token)):
    db_request = await service.update_request(request_id=request_id, request_data=request)
    if db_request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    return db_request

@router.delete("/{request_id}")
async def delete_request(request_id: str, service: RequestService = Depends(get_request_service), credentials: HTTPAuthorizationCredentials = Depends(verify_token)):
    await service.delete_request(request_id=request_id)
    return {"detail": "Request deleted"}

@router.get("/{request_id}/scraps", response_model=List[Scrap])
async def get_request(request_id: str, service: ScrapService = Depends(get_scrap_service), credentials: HTTPAuthorizationCredentials = Depends(verify_token)):
    db_request = await service.get_all_scraps()
    if db_request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    return db_request
