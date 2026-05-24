from __future__ import annotations

from pathlib import Path

from app.main import app


def test_pms_projection_monolith_files_are_removed() -> None:
    removed_files = {
        "app/api/routes/backoffice/pms_projection.py",
        "app/domains/pms_projection/models/pms_projection.py",
        "app/domains/pms_projection/contracts/pms_projection_contract.py",
        "app/domains/pms_projection/repos/pms_projection_repo.py",
        "app/domains/pms_projection/services/pms_projection_service.py",
    }

    for file_path in removed_files:
        assert not Path(file_path).exists()


def test_pms_projection_vertical_modules_exist() -> None:
    expected = {
        "products.py",
        "units.py",
        "sku_codes.py",
        "barcodes.py",
        "item_contents.py",
        "item_assets.py",
        "display_categories.py",
        "category_bindings.py",
        "brand_profiles.py",
        "brand_assets.py",
        "sync_runs.py",
    }

    for package in [
        Path("app/domains/pms_projection/models"),
        Path("app/domains/pms_projection/contracts"),
        Path("app/domains/pms_projection/repos"),
        Path("app/domains/pms_projection/services"),
        Path("app/api/routes/backoffice/pms_projection"),
    ]:
        actual = {path.name for path in package.glob("*.py")}
        assert expected.issubset(actual)


def test_pms_projection_http_paths_remain_stable_after_vertical_split() -> None:
    paths = {
        str(getattr(route, "path", ""))
        for route in app.routes
        if isinstance(getattr(route, "path", ""), str)
    }

    assert {
        "/backoffice/pms-projections/health",
        "/backoffice/pms-projections/products",
        "/backoffice/pms-projections/units",
        "/backoffice/pms-projections/sku-codes",
        "/backoffice/pms-projections/barcodes",
        "/backoffice/pms-projections/item-contents",
        "/backoffice/pms-projections/item-assets",
        "/backoffice/pms-projections/display-categories",
        "/backoffice/pms-projections/item-display-category-bindings",
        "/backoffice/pms-projections/brand-profiles",
        "/backoffice/pms-projections/brand-assets",
        "/backoffice/pms-projections/sync-runs",
    }.issubset(paths)
