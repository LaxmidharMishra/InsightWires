# api/routers/business_events.py
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from util.taxonomy_reader import taxonomy_reader
from api.core.security import verify_api_key

router = APIRouter(prefix="/sentiments", tags=["Sentiments"])

@router.get("/")
async def get_sentiments(
    api_key: str = Depends(verify_api_key)
) -> Dict[str, Any]:
    """Get all sentiments taxonomy data"""
    try:
        results = taxonomy_reader.search_taxonomy(
            'sentiments',
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
            detail="Sentiments taxonomy not found"
        )