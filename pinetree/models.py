from typing import Any, List

from pydantic import BaseModel

RenderedTemplate = str
JobJson = dict


class JobVars(BaseModel):
    name: str
    image: str
    port: int
    datacenter: str = "dc1"


class Alloc(BaseModel):
    ID: str
    ParentID: str
    Name: str
    Namespace: str
    Datacenters: List[str]
    NodePool: str
    Multiregion: Any
    Type: str
    Priority: int
    Periodic: bool
    ParameterizedJob: bool
    Stop: bool
    Status: str
    StatusDescription: str
    JobSummary: dict
    CreateIndex: int
    ModifyIndex: int
    JobModifyIndex: int
    SubmitTime: int
    Meta: Any
