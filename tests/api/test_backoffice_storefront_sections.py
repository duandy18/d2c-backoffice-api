from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

BACKOFFICE_HEADERS = {"X-Backoffice-Client": "d2c-backoffice-web"}


def test_storefront_sections_require_backoffice_client() -> None:
    client = TestClient(app)

    response = client.get("/backoffice/storefront-sections")

    assert response.status_code == 401
    assert response.json() == {"detail": "backoffice_client_required"}


def test_storefront_sections_create_and_layout() -> None:
    client = TestClient(app)
    section_code = f"section-pytest-cat-litter-{uuid4().hex[:8]}"

    response = client.post(
        "/backoffice/storefront-sections",
        headers=BACKOFFICE_HEADERS,
        json={
            "section_code": section_code,
            "section_type": "offer_shelf",
            "group_code": "cat_litter",
            "title": "猫砂专区",
            "subtitle": "高复购猫砂",
            "sort_order": 20,
        },
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["section_code"] == section_code
    assert payload["group_code"] == "cat_litter"
    assert payload["title"] == "猫砂专区"

    layout_response = client.post(
        f"/backoffice/storefront-sections/{section_code}/layout",
        headers=BACKOFFICE_HEADERS,
        json={
            "display_type": "product_grid",
            "columns_desktop": 4,
            "columns_tablet": 2,
            "columns_mobile": 1,
            "card_size": "standard",
            "image_ratio": "1:1",
            "show_promotion_badge": True,
            "show_sales_summary": True,
            "show_review_summary": True,
            "show_compare_price": True,
            "show_quantity_stepper": True,
            "max_items": 12,
        },
    )

    assert layout_response.status_code == 200
    layout = layout_response.json()
    assert layout["section_code"] == section_code
    assert layout["display_type"] == "product_grid"
    assert layout["columns_desktop"] == 4
    assert layout["max_items"] == 12

    list_response = client.get("/backoffice/storefront-sections", headers=BACKOFFICE_HEADERS)
    assert list_response.status_code == 200
    sections = {row["section_code"]: row for row in list_response.json()["sections"]}
    assert section_code in sections


def test_storefront_section_create_rejects_missing_group() -> None:
    client = TestClient(app)

    response = client.post(
        "/backoffice/storefront-sections",
        headers=BACKOFFICE_HEADERS,
        json={
            "section_code": f"section-pytest-missing-group-{uuid4().hex[:8]}",
            "section_type": "offer_shelf",
            "group_code": "missing-group",
            "title": "Missing",
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "group_not_found"}
