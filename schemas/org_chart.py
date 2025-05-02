from pydantic import BaseModel, Field
from uuid import UUID


class OrgChartBase(BaseModel):
    """
    OrgChart is a Pydantic model that represents an organizational chart.
    It contains information about the organization, including its name
    and an id.
    """

    name: str = Field(..., description="The name of the organization.")


class OrgChartCreate(OrgChartBase):
    """
    OrgChart is a Pydantic model that represents an organizational chart.
    It contains information about the organization, including its name
    and an id.
    """

    pass


class OrgChartRead(OrgChartBase):
    """
    OrgChart is a Pydantic model that represents an organizational chart.
    It contains information about the organization, including its name
    and an id.
    """

    id: UUID = Field(
        ..., description="The unique identifier for the organization."
    )
    name: str = Field(
        ..., description="The name of the organization."
    )

    class Config:
        orm_mode = True


class OrgChartUpdate(OrgChartBase):
    """
    OrgChart is a Pydantic model that represents an organizational chart.
    It contains information about the organization, including its name
    and an id.
    """

    pass

class OrgChartDelete(BaseModel):
    """
    OrgChart is a Pydantic model that represents an organizational chart.
    It contains information about the organization, including its name
    and an id.
    """

    id: UUID = Field(
        ..., description="The unique identifier for the organization."
    )