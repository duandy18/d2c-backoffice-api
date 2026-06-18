from __future__ import annotations

import ast
from pathlib import Path


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


def _literal_string(node: ast.AST) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None


def _join_paths(*parts: str) -> str:
    cleaned = [part.strip("/") for part in parts if part.strip("/")]
    return "/" + "/".join(cleaned)


def _router_prefix(module_path: Path) -> str:
    tree = ast.parse(module_path.read_text())
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue

        target_names = {
            target.id
            for target in node.targets
            if isinstance(target, ast.Name)
        }
        if "router" not in target_names or not isinstance(node.value, ast.Call):
            continue

        for keyword in node.value.keywords:
            if keyword.arg == "prefix":
                return _literal_string(keyword.value) or ""

    return ""


def _module_route_paths(module_path: Path) -> set[str]:
    tree = ast.parse(module_path.read_text())
    module_prefix = _router_prefix(module_path)
    paths: set[str] = set()

    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue

        for decorator in node.decorator_list:
            if not isinstance(decorator, ast.Call):
                continue
            if not isinstance(decorator.func, ast.Attribute):
                continue
            if decorator.func.attr.lower() not in {"delete", "get", "patch", "post", "put"}:
                continue

            route_path = ""
            if decorator.args:
                route_path = _literal_string(decorator.args[0]) or ""
            for keyword in decorator.keywords:
                if keyword.arg == "path":
                    route_path = _literal_string(keyword.value) or route_path

            paths.add(_join_paths(module_prefix, route_path))

    return paths


def test_pms_projection_http_paths_remain_stable_after_vertical_split() -> None:
    parent_router_path = Path("app/api/routes/backoffice/pms_projection/router.py")
    parent_prefix = _router_prefix(parent_router_path)
    assert parent_prefix == "/backoffice/pms-projections"

    module_names = {
        "barcodes",
        "health",
        "products",
        "sku_codes",
        "sync_runs",
        "units",
    }
    parent_router_source = parent_router_path.read_text()
    for module_name in module_names:
        assert module_name in parent_router_source

    child_paths: set[str] = set()
    for module_name in module_names:
        child_paths.update(
            _module_route_paths(
                Path(f"app/api/routes/backoffice/pms_projection/{module_name}.py")
            )
        )

    paths = {_join_paths(parent_prefix, child_path) for child_path in child_paths}

    assert {
        "/backoffice/pms-projections/health",
        "/backoffice/pms-projections/products",
        "/backoffice/pms-projections/units",
        "/backoffice/pms-projections/sku-codes",
        "/backoffice/pms-projections/barcodes",
        "/backoffice/pms-projections/sync-runs",
    }.issubset(paths)
