from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional


class EmployeeBase(BaseModel):
    """
    Employee is a Pydantic model for employee creation that represents an employee
    with an organization.
    It contains information about the employee's name, organization, manager's id,
    and own id.
    """

    name: str = Field(..., description="The name of the employee.")
    manager_id: Optional[UUID] = Field(
        default=None, description="The unique identifier for the employee's manager."
    )


class EmployeeCreate(EmployeeBase):
    """
    Employee is a Pydantic model for employee creation that represents an employee
    with an organization.
    It contains information about the employee's name, organization, manager's id,
    and own id.
    """

    pass


class EmployeeRead(EmployeeBase):
    """
    Employee is a Pydantic model for employee read that represents an employee
    with an organization.
    It contains information about the employee's name, organization, manager's id,
    and own id.
    """

    id: UUID = Field(
        ..., description="The unique identifier for the employee."
    )

    class Config:
        orm_mode = True


class EmployeeUpdate(EmployeeBase):
    """
    Employee is a Pydantic model for employee update that represents an employee
    with an organization.
    It contains information about the employee's name, organization, manager's id,
    and own id.
    """

    pass

class EmployeeDelete(BaseModel):
    """
    Employee is a Pydantic model for employee deletion that represents an employee
    with an organization.
    It contains information about the employee's name, organization, manager's id,
    and own id.
    """

    id: UUID = Field(
        ..., description="The unique identifier for the employee."
    )