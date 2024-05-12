from pydantic import BaseModel

RenderedTemplate = str
JobJson = dict


class JobVars(BaseModel):
    name: str
    image: str
    port: int
    datacenter: str = "dc1"
