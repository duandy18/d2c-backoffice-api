"""Shared display-table contract for PMS projection read APIs."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

PmsProjectionColumnKind = Literal[
    "text",
    "number",
    "boolean",
    "status",
    "datetime",
    "url",
    "image",
    "json",
]


class PmsProjectionTableColumn(BaseModel):
    key: str
    label: str
    kind: PmsProjectionColumnKind = "text"
    source_field: str | None = None


class PmsProjectionDisplayTable(BaseModel):
    resource: str
    projection_table: str
    columns: list[PmsProjectionTableColumn] = Field(default_factory=list)
    rows: list[dict[str, Any]] = Field(default_factory=list)


__all__ = [
    "PmsProjectionColumnKind",
    "PmsProjectionDisplayTable",
    "PmsProjectionTableColumn",
]
