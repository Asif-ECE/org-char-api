from sqlmodel import SQLModel, Field, Relationship
from typing import List, TYPE_CHECKING
from uuid import UUID, uuid4

if TYPE_CHECKING:
    from .employee import Employee

class OrgChart(SQLModel, table=True):
    """
    OrgChart is a SQLModel that represents an organizational chart.
    It contains information about the organization, including its name,
    an id and employees work here.
    """

    __tablename__ = "org_chart"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        description="The unique identifier for the organization."
    )
    name: str = Field(..., description="The name of the organization.")
    employee: List["Employee"] = Relationship(
        back_populates="org_chart",
        cascade_delete=True,
    )