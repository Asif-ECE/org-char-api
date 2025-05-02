from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from uuid import UUID, uuid4

if TYPE_CHECKING:
    from .org_chart import OrgChart

class Employee(SQLModel, table=True):
    """
    Employee is a SQLModel that represents an employee with an organization.
    It contains information about the employee's name, organization, manager's id,
    and direct reports.
    """

    __tablename__ = "employee"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        description="The unique identifier for the employee."
    )
    org_id: UUID = Field(
        ...,
        description="The unique identifier for the organization.",
        foreign_key="org_chart.id"
    )
    name: str = Field(..., description="The name of the employee.")
    manager_id: Optional[UUID] = Field(
        default=None,
        foreign_key="employee.id",
        description="The unique identifier for the employee's manager."
    )

    org_chart: "OrgChart" = Relationship(
        back_populates="employee"
    )
    direct_reports: List["Employee"] = Relationship(
        back_populates="manager",
        sa_relationship_kwargs={"passive_deletes": True},
    )
    manager: Optional["Employee"] = Relationship(
        back_populates="direct_reports",
        sa_relationship_kwargs={"remote_side": "Employee.id", "passive_deletes": True}
    )