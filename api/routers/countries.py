# api/routers/business_events.py
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from util.taxonomy_reader import taxonomy_reader
from api.core.security import verify_api_key

router = APIRouter(prefix="/countries", tags=["Countries"])

@router.get("/")
async def get_countries(
    api_key: str = Depends(verify_api_key)
) -> Dict[str, Any]:
    """Get all countries taxonomy data"""
    try:
        results = taxonomy_reader.search_taxonomy(
            'countries',
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
            detail="Countries taxonomy not found"
        )