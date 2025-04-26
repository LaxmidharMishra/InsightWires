# api/routers/companies.py
from fastapi import APIRouter, Query, HTTPException, Body, Depends
from typing import Optional, Dict, Any
from util.taxonomy_reader import taxonomy_reader
from pydantic import BaseModel
from api.core.security import verify_api_key

router = APIRouter(prefix="/companies", tags=["Company"])

class CompanyRequest(BaseModel):
    company_name: Optional[str] = None
    company_url: Optional[str] = None

@router.get("/search")
async def search_companies(
    name: Optional[str] = Query(None, description="Search by company name"),
    url: Optional[str] = Query(None, description="Search by company URL"),
    api_key: str = Depends(verify_api_key)
) -> Dict[str, Any]:
    """
    Search companies by name or URL. 
    - name: searches in company_name field
    - url: searches in company_url field
    At least one parameter (name or URL) must be provided.
    """
    # Check if both parameters are empty
    if not name and not url:
        raise HTTPException(
            status_code=400,
            detail="Please enter a valid name or URL to search for"
        )

    try:
        results = taxonomy_reader.search_companies(name=name, url=url)
        
        # If search was performed but no results found
        if len(results) == 0:
            search_term = name if name else url
            raise HTTPException(
                status_code=404,
                detail={
                    "message": f"We don't have this company details with us. Please verify the details you provided: {search_term}",
                    "suggestion": "You can request to add this company using the /companies/request endpoint"
                }
            )

        return {
            "total_count": len(results),
            "data": results
        }
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail="Companies taxonomy not found"
        )

@router.post("/request")
async def request_company(
    company: CompanyRequest,
    api_key: str = Depends(verify_api_key)
) -> Dict[str, Any]:
    """
    Request to add a new company that's not in our database.
    Provide either company name or URL or both.
    """
    if not company.company_name and not company.company_url:
        raise HTTPException(
            status_code=400,
            detail="Please provide either company name or URL or both"
        )

    try:
        # First check if company already exists
        existing = taxonomy_reader.search_companies(
            name=company.company_name, 
            url=company.company_url
        )
        
        if existing:
            raise HTTPException(
                status_code=400,
                detail="This company already exists in our database"
            )

        # Add the request
        new_request = taxonomy_reader.add_company_request(
            company_name=company.company_name,
            company_url=company.company_url
        )
        
        return {
            "message": "Company request submitted successfully",
            "request": new_request
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to submit company request: {str(e)}"
        )