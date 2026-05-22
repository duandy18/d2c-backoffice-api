from __future__ import annotations

from fastapi.routing import APIRoute

from app.main import app


def main() -> None:
    routes = []
    for route in app.routes:
        if isinstance(route, APIRoute):
            methods = ",".join(sorted(route.methods))
            routes.append((route.path, methods, route.name))

    for path, methods, name in sorted(routes):
        print(f"{methods:12s} {path:40s} {name}")


if __name__ == "__main__":
    main()
