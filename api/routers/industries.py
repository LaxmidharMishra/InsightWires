# api/routers/business_events.py
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from util.taxonomy_reader import taxonomy_reader
from api.core.security import verify_api_key

router = APIRouter(prefix="/industries", tags=["Industries"])

@router.get("/")
async def get_industries(
    api_key: str = Depends(verify_api_key)
) -> Dict[str, Any]:
    """Get all industries taxonomy data"""
    try:
        results = taxonomy_reader.search_taxonomy(
            'industries',
            search_term=None,
            field=None
        )
        return {
            "total_count": len(results),
            "data": results
        }
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail="Industries taxonomy not found"
        )