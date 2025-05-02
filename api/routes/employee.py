from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from db.session import get_session
from schemas.employee import EmployeeCreate, EmployeeRead
from crud import employee as emp_crud
from uuid import UUID
from services.organization import promote_employee_to_ceo

router = APIRouter(prefix="/org_charts/{org_id}/employees", tags=["Employees"])

@router.post("/", response_model=EmployeeRead)
async def create_employee(org_id: UUID, emp: EmployeeCreate, db: AsyncSession = Depends(get_session)):
    return await emp_crud.create_employee(db, org_id, emp)

@router.get("/", response_model=list[EmployeeRead])
async def get_employees_by_org(org_id: UUID, db: AsyncSession = Depends(get_session)):
    employees = await emp_crud.get_employees_by_org(db, org_id)
    if not employees:
        raise HTTPException(status_code=404, detail="No employees found for this organization")
    return employees

@router.get("/{id}/", response_model=EmployeeRead)
async def get_employee(id: UUID, db: AsyncSession = Depends(get_session)):
    emp = await emp_crud.get_employee(db, id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp

@router.put("/{id}/", response_model=EmployeeRead)
async def update_employee(id: UUID, org_id: UUID, new_manager_id: UUID, db: AsyncSession = Depends(get_session)):
    emp = await emp_crud.update_employee_manager(db, id, new_manager_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp

@router.delete("/{id}/")
async def delete_employee(id: UUID, org_id: UUID, db: AsyncSession = Depends(get_session)):
    emp = await emp_crud.get_employee(db, id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    await emp_crud.delete_employee(db, id)
    return {"detail": "Employee deleted successfully"}

@router.post("/{id}/promote")
async def promote_employee(id: UUID, org_id: UUID, db: AsyncSession = Depends(get_session)):
    emp = await promote_employee_to_ceo(db, id, org_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp
