from __future__ import annotations

import argparse
import json
from dataclasses import asdict

from app.core.config import load_settings
from app.core.database import get_session_factory
from app.domains.pms_projection.clients.pms_projection_feed_client import PmsProjectionFeedClient
from app.domains.pms_projection.services.pms_projection_sync_service import (
    PMS_PROJECTION_SYNC_SCOPES,
    PmsProjectionSyncService,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync PMS projection feeds into D2C backoffice.")
    parser.add_argument(
        "--scope",
        choices=("all", *PMS_PROJECTION_SYNC_SCOPES),
        default="all",
    )
    parser.add_argument("--requested-by", default="local-script")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    settings = load_settings()
    session_factory = get_session_factory(settings.database_url)

    client = PmsProjectionFeedClient(
        base_url=settings.pms_api_base_url,
        service_client_code=settings.pms_service_client_code,
        page_limit=settings.pms_projection_sync_page_limit,
    )

    with session_factory() as session:
        service = PmsProjectionSyncService(session=session, feed_reader=client)
        if args.scope == "all":
            result = service.sync_all(requested_by=args.requested_by)
        else:
            scope_result = service.sync_scope(args.scope, requested_by=args.requested_by)
            result = type(
                "SingleScopeResult",
                (),
                {
                    "status": scope_result.status,
                    "scopes": [scope_result],
                },
            )()

    payload = {
        "status": result.status,
        "scopes": [asdict(scope) for scope in result.scopes],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2, default=str))

    if result.status != "success":
        raise RuntimeError("PMS projection sync failed")


if __name__ == "__main__":
    main()
