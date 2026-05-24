"""PMS brand profile projection service."""

from sqlalchemy.orm import Session

from app.domains.pms_projection.contracts.brand_profiles import (
    PmsBrandProfileProjectionContract,
    PmsBrandProfilesProjectionResponse,
)
from app.domains.pms_projection.models.brand_profiles import PmsBrandProfileProjection
from app.domains.pms_projection.repos.brand_profiles import list_brand_profile_projections


def _build_brand_profile(row: PmsBrandProfileProjection) -> PmsBrandProfileProjectionContract:
    return PmsBrandProfileProjectionContract(
        id=row.id,
        pms_profile_id=row.pms_profile_id,
        brand_id=row.brand_id,
        brand_code=row.brand_code,
        brand_name=row.brand_name,
        display_name=row.display_name,
        official_name=row.official_name,
        brand_story=row.brand_story,
        country_or_region=row.country_or_region,
        website_url=row.website_url,
        seo_title=row.seo_title,
        seo_description=row.seo_description,
        status=row.status,
        pms_updated_at=row.pms_updated_at,
        synced_at=row.synced_at,
        raw_payload=row.raw_payload,
    )


def get_pms_brand_profile_projections(session: Session) -> PmsBrandProfilesProjectionResponse:
    rows = [_build_brand_profile(row) for row in list_brand_profile_projections(session)]
    return PmsBrandProfilesProjectionResponse(count=len(rows), brand_profiles=rows)


__all__ = ["get_pms_brand_profile_projections"]
