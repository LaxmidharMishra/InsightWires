from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List, Dict, Any
from util.taxonomy_reader import taxonomy_reader

router = APIRouter(prefix="/taxonomy", tags=["Taxonomy"])

@router.get("/{taxonomy_name}")
async def get_taxonomy(
    taxonomy_name: str,
    search: Optional[str] = Query(None, description="Search term"),
    field: Optional[str] = Query(None, description="Specific field to search in")
) -> Dict[str, Any]:
    """Get taxonomy data with optional search"""
    try:
        results = taxonomy_reader.search_taxonomy(taxonomy_name, search, field)
        return {
            "total_count": len(results),
            "data": results
        }
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail=f"Taxonomy {taxonomy_name} not found"
        )
