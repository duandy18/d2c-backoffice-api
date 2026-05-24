"""PMS projection health contracts."""

from pydantic import BaseModel


class PmsProjectionHealthResponse(BaseModel):
    status: str
    module: str
    surface: str


__all__ = ["PmsProjectionHealthResponse"]
