import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from api.models import (
    InsightWire, 
    BusinessActivityMapping, 
    CompanyMapping, 
    IndustryTypeMapping,
    ContentTypeMapping,
    SourceTypeMapping,
    SentimentTypeMapping
)
from sqlalchemy import select
import json
from typing import List, Dict
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

async def migrate_data():
    # Create engine and session
    engine = create_async_engine(DATABASE_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        # Get all records from InsightWire
        stmt = select(InsightWire)
        result = await session.execute(stmt)
        records = result.scalars().all()

        for record in records:
            current_time = datetime.utcnow()

            # Handle business activities
            if record.business_activities:
                try:
                    activities = json.loads(record.business_activities)
                    if isinstance(activities, list):
                        for activity in activities:
                            if isinstance(activity, dict):
                                mapping = BusinessActivityMapping(
                                    insightwire_uuid=str(record.uuid),
                                    business_activity_id=activity.get('id', 0),
                                    system_timestamp=current_time
                                )
                                session.add(mapping)
                except json.JSONDecodeError:
                    # Handle case where business_activities is a string
                    mapping = BusinessActivityMapping(
                        insightwire_uuid=str(record.uuid),
                        business_activity_id=record.business_activity_id or 0,
                        system_timestamp=current_time
                    )
                    session.add(mapping)

            # Handle companies
            if record.companies:
                try:
                    companies = json.loads(record.companies)
                    if isinstance(companies, list):
                        for company in companies:
                            if isinstance(company, dict):
                                mapping = CompanyMapping(
                                    insightwire_uuid=str(record.uuid),
                                    company_id=company.get('id', 0),
                                    system_timestamp=current_time
                                )
                                session.add(mapping)
                except json.JSONDecodeError:
                    # Handle case where companies is a string
                    mapping = CompanyMapping(
                        insightwire_uuid=str(record.uuid),
                        company_id=0,
                        system_timestamp=current_time
                    )
                    session.add(mapping)

            # Handle industries
            if record.industries:
                try:
                    industries = json.loads(record.industries)
                    if isinstance(industries, list):
                        for industry in industries:
                            if isinstance(industry, dict):
                                mapping = IndustryTypeMapping(
                                    insightwire_uuid=str(record.uuid),
                                    industry_type_id=industry.get('id', 0),
                                    system_timestamp=current_time
                                )
                                session.add(mapping)
                except json.JSONDecodeError:
                    # Handle case where industries is a string
                    mapping = IndustryTypeMapping(
                        insightwire_uuid=str(record.uuid),
                        industry_type_id=record.industry_type_id or 0,
                        system_timestamp=current_time
                    )
                    session.add(mapping)

            # Handle content type
            if record.content_type_id:
                mapping = ContentTypeMapping(
                    insightwire_uuid=str(record.uuid),
                    content_type_id=record.content_type_id,
                    system_timestamp=current_time
                )
                session.add(mapping)

            # Handle source type
            if record.source_type_id:
                mapping = SourceTypeMapping(
                    insightwire_uuid=str(record.uuid),
                    source_type_id=record.source_type_id,
                    system_timestamp=current_time
                )
                session.add(mapping)

            # Handle sentiment type
            if record.sentiment_type_id:
                mapping = SentimentTypeMapping(
                    insightwire_uuid=str(record.uuid),
                    sentiment_type_id=record.sentiment_type_id,
                    system_timestamp=current_time
                )
                session.add(mapping)

        # Commit the changes
        await session.commit()

if __name__ == "__main__":
    asyncio.run(migrate_data()) 