from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from db.session import get_session
from schemas.org_chart import OrgChartCreate, OrgChartRead
from crud import org_chart as org_crud
from uuid import UUID


router = APIRouter(prefix="/orgcharts", tags=["Org Charts"])

@router.post("/", response_model=OrgChartRead)
async def create_org(org: OrgChartCreate, db: AsyncSession = Depends(get_session)):
    return await org_crud.create_org_chart(db, org)

@router.get("/", response_model=list[OrgChartRead])
async def get_all_orgs(db: AsyncSession = Depends(get_session)):
    return await org_crud.get_all_org_charts(db)

@router.get("/{org_id}", response_model=OrgChartRead)
async def get_org(org_id: UUID, db: AsyncSession = Depends(get_session)):
    org = await org_crud.get_org_chart(db, org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Org not found")
    return org

@router.delete("/{org_id}")
async def delete_org(org_id: UUID, db: AsyncSession = Depends(get_session)):
    org = await org_crud.get_org_chart(db, org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Org not found")
    await org_crud.delete_org_chart(db, org_id)
    return {"detail": "Org deleted successfully"}

@router.put("/{org_id}", response_model=OrgChartRead)
async def update_org(org_id: UUID, org: OrgChartCreate, db: AsyncSession = Depends(get_session)):
    existing_org = await org_crud.get_org_chart(db, org_id)
    if not existing_org:
        raise HTTPException(status_code=404, detail="Org not found")
    updated_org = await org_crud.update_org_chart(db, org_id, org)
    return updated_org
