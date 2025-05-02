from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from models.org_chart import OrgChart
from schemas.org_chart import OrgChartCreate, OrgChartUpdate

async def create_org_chart(db: AsyncSession, org: OrgChartCreate) -> OrgChart:
    db_org = OrgChart(**org.model_dump())
    db.add(db_org)
    await db.commit()
    await db.refresh(db_org)
    return db_org

async def get_org_chart(db: AsyncSession, org_id: str) -> OrgChart | None:
    return await db.get(OrgChart, org_id)

async def get_all_org_charts(db: AsyncSession):
    result = await db.execute(select(OrgChart))
    return result.scalars().all()

async def delete_org_chart(db: AsyncSession, org_id: str):
    org = await db.get(OrgChart, org_id)
    if org:
        await db.delete(org)
        await db.commit()

async def update_org_chart(db: AsyncSession, org_id: str, org: OrgChartUpdate) -> OrgChart:
    db_org = await db.get(OrgChart, org_id)
    if db_org:
        for key, value in org.model_dump().items():
            setattr(db_org, key, value)
        db.add(db_org)
        await db.commit()
        await db.refresh(db_org)
        return db_org
    return None
