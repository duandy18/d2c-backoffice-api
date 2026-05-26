"""PMS projection feed HTTP client."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError
from urllib.parse import urlencode, urljoin
from urllib.request import Request, urlopen

PMS_SERVICE_CLIENT_HEADER = "X-Service-Client"

PmsProjectionScope = str

_SCOPE_ENDPOINTS: dict[PmsProjectionScope, str] = {
    "products": "/pms/read/v1/projection-feed/items",
    "units": "/pms/read/v1/projection-feed/uoms",
    "sku_codes": "/pms/read/v1/projection-feed/sku-codes",
    "barcodes": "/pms/read/v1/projection-feed/barcodes",
}


@dataclass(frozen=True)
class PmsProjectionFeedPage:
    endpoint: str
    rows: list[dict[str, Any]]
    limit: int
    offset: int
    next_offset: int | None
    has_more: bool


class PmsProjectionFeedClientError(RuntimeError):
    pass


class PmsProjectionFeedClient:
    def __init__(
        self,
        *,
        base_url: str,
        service_client_code: str,
        page_limit: int = 500,
        timeout_seconds: float = 15.0,
    ) -> None:
        self.base_url = base_url.rstrip("/") + "/"
        self.service_client_code = service_client_code
        self.page_limit = max(1, min(int(page_limit), 500))
        self.timeout_seconds = timeout_seconds

    def endpoint_for_scope(self, scope: PmsProjectionScope) -> str:
        try:
            return _SCOPE_ENDPOINTS[scope]
        except KeyError as exc:
            raise ValueError(f"unsupported PMS projection sync scope: {scope}") from exc

    def fetch_page(
        self,
        *,
        scope: PmsProjectionScope,
        limit: int,
        offset: int,
    ) -> PmsProjectionFeedPage:
        endpoint = self.endpoint_for_scope(scope)
        query = urlencode({"limit": int(limit), "offset": int(offset)})
        url = urljoin(self.base_url, endpoint.lstrip("/"))
        request = Request(
            f"{url}?{query}",
            headers={
                PMS_SERVICE_CLIENT_HEADER: self.service_client_code,
                "Accept": "application/json",
            },
            method="GET",
        )

        try:
            with urlopen(request, timeout=self.timeout_seconds) as response:
                raw = response.read().decode("utf-8")
        except HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise PmsProjectionFeedClientError(
                f"PMS projection feed HTTP {exc.code} for {endpoint}: {body}"
            ) from exc

        payload = json.loads(raw)
        rows = payload.get("rows")
        if not isinstance(rows, list):
            raise PmsProjectionFeedClientError(f"PMS projection feed {endpoint} missing rows list")

        return PmsProjectionFeedPage(
            endpoint=endpoint,
            rows=[dict(row) for row in rows],
            limit=int(payload.get("limit") or limit),
            offset=int(payload.get("offset") or offset),
            next_offset=payload.get("next_offset"),
            has_more=bool(payload.get("has_more")),
        )

    def fetch_all(self, scope: PmsProjectionScope) -> tuple[str, list[dict[str, Any]]]:
        offset = 0
        all_rows: list[dict[str, Any]] = []
        endpoint = self.endpoint_for_scope(scope)

        while True:
            page = self.fetch_page(
                scope=scope,
                limit=self.page_limit,
                offset=offset,
            )
            endpoint = page.endpoint
            all_rows.extend(page.rows)

            if not page.has_more or page.next_offset is None:
                break

            offset = int(page.next_offset)

        return endpoint, all_rows


__all__ = [
    "PMS_SERVICE_CLIENT_HEADER",
    "PmsProjectionFeedClient",
    "PmsProjectionFeedClientError",
    "PmsProjectionFeedPage",
]
