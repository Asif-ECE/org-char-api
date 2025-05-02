from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import Employee
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


async def promote_employee_to_ceo(session: AsyncSession, employee_id: UUID, org_id: UUID):
    """
    Promote an employee to CEO of the organization.
    """
    # Fetch the employee from the database
    result = await session.exec(select(Employee).where(Employee.id == employee_id))
    employee = result.scalar_one_or_none()

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found."
        )

    # Check if the employee belongs to the organization
    if employee.org_id != org_id:
        raise HTTPException(
            status_code=404,
            detail="Employee does not belong to this organization."
        )

    # Check if the employee is already a CEO
    if employee.manager_id is None:
        raise HTTPException(
            status_code=400,
            detail="Employee is already a CEO."
        )

    # Fetch the current CEO of the organization
    previous_ceo_result = await session.execute(
        select(Employee).where(Employee.manager_id == None, Employee.org_id == org_id)
    )
    previous_ceo = previous_ceo_result.scalar_one_or_none()

    # Update the employee's role to CEO
    employee.manager_id = None

    if previous_ceo:
        # Reassign the previous CEO's direct reports to the new CEO
        previous_ceo_reports_result = await session.execute(
            select(Employee).where(Employee.manager_id == previous_ceo.id)
        )
        previous_ceo_reports = previous_ceo_reports_result.scalars().all()
        for report in previous_ceo_reports:
            report.manager_id = employee.id

        # Reassign the new CEO's old direct reports to the previous CEO
        new_ceo_old_reports_result = await session.execute(
            select(Employee).where(Employee.manager_id == employee.id)
        )
        new_ceo_old_reports = new_ceo_old_reports_result.scalars().all()
        for report in new_ceo_old_reports:
            report.manager_id = previous_ceo.id

        # Make the previous CEO report to the new CEO
        previous_ceo.manager_id = employee.id

    # Commit the transaction atomically
    try:
        await session.commit()
        await session.refresh(employee)
    except Exception:
        await session.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to promote employee to CEO."
        )

    return employee