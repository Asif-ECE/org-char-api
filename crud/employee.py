from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from models.employee import Employee
from schemas.employee import EmployeeCreate
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

async def create_employee(db: AsyncSession, org_id: UUID, emp: EmployeeCreate) -> Employee:
    async with db.begin():
        if emp.manager_id is None:
            result = await db.execute(select(Employee).where(Employee.org_id == org_id))
            existing_employee = result.scalars().first()
            if existing_employee:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Manager ID cannot be null if there is at least one employee."
                )

        db_emp = Employee(**emp.model_dump(), org_id=org_id)
        db.add(db_emp)
        try:
            await db.commit()
            await db.refresh(db_emp)
            return db_emp
        except IntegrityError as e:
            await db.rollback()
            if "FOREIGN KEY constraint failed" in str(e.orig):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid organization ID or manager ID. Make sure both exist."
                )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create employee due to database constraint."
            )

async def get_employee(db: AsyncSession, org_id: UUID, emp_id: UUID) -> Employee | None:
    emp = await db.get(Employee, emp_id)
    if emp and emp.org_id != org_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found in the specified organization."
        )
    return emp

async def get_employees_by_org(db: AsyncSession, org_id: UUID):
    result = await db.execute(select(Employee).where(Employee.org_id == org_id))
    return result.scalars().all()

async def update_employee(db: AsyncSession, org_id: UUID, emp_id: UUID, new_manager_id: UUID = None, new_name: str = None):
    async with db.begin():
        emp = await db.get(Employee, emp_id)
        if not emp or emp.org_id != org_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found in the specified organization."
            )

        if new_manager_id:
            current_manager_id = new_manager_id
            while current_manager_id:
                if current_manager_id == emp_id:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Circular manager reference detected."
                    )
                manager = await db.get(Employee, current_manager_id)
                if manager and manager.org_id != org_id:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Manager must belong to the same organization."
                    )
                current_manager_id = manager.manager_id if manager else None

            emp.manager_id = new_manager_id

        if new_name:
            emp.name = new_name

        await db.commit()
        await db.refresh(emp)
        return emp

async def delete_employee(db: AsyncSession, org_id: UUID, emp_id: UUID):
    async with db.begin():
        emp = await db.get(Employee, emp_id)
        if not emp or emp.org_id != org_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found in the specified organization."
            )

        if emp.manager_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CEO cannot be deleted."
            )

        result = await db.execute(select(Employee).where(Employee.manager_id == emp_id, Employee.org_id == org_id))
        direct_reports = result.scalars().all()
        for report in direct_reports:
            report.manager_id = emp.manager_id

        await db.delete(emp)
        await db.commit()
