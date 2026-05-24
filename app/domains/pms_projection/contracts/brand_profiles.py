"""PMS brand profile projection contracts."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class PmsBrandProfileProjectionContract(BaseModel):
    id: int
    pms_profile_id: int
    brand_id: int
    brand_code: str | None
    brand_name: str | None
    display_name: str | None
    official_name: str | None
    brand_story: str | None
    country_or_region: str | None
    website_url: str | None
    seo_title: str | None
    seo_description: str | None
    status: str
    pms_updated_at: datetime | None
    synced_at: datetime
    raw_payload: dict[str, Any] | None


class PmsBrandProfilesProjectionResponse(BaseModel):
    count: int = Field(..., ge=0)
    brand_profiles: list[PmsBrandProfileProjectionContract]


__all__ = ["PmsBrandProfileProjectionContract", "PmsBrandProfilesProjectionResponse"]
