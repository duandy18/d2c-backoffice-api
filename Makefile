PYTHON ?= python3
VENV_PYTHON ?= .venv/bin/python3

D2C_BACKOFFICE_ENV ?= local
HOST ?= 0.0.0.0
PORT ?= 8026
PID_FILE ?= /tmp/d2c_backoffice_api_8026.pid
LOG_FILE ?= /tmp/d2c_backoffice_api_8026.log
HEALTH_URL ?= http://127.0.0.1:$(PORT)/system/health

DEV_DB_DSN ?= postgresql+psycopg://d2c_backoffice:d2c_backoffice@127.0.0.1:5433/d2c_backoffice
DEV_TEST_DB_DSN ?= postgresql+psycopg://d2c_backoffice:d2c_backoffice@127.0.0.1:5433/d2c_backoffice_test

PMS_API_BASE_URL ?= http://127.0.0.1:8002
PMS_SERVICE_CLIENT_CODE ?= d2c-backoffice-service
PMS_PROJECTION_SYNC_PAGE_LIMIT ?= 500
PMS_PROJECTION_SYNC_REQUESTED_BY ?= make

DEV_ENV := D2C_BACKOFFICE_ENVIRONMENT="$(D2C_BACKOFFICE_ENV)" D2C_BACKOFFICE_DATABASE_URL="$(DEV_DB_DSN)" D2C_BACKOFFICE_TEST_DATABASE_URL="$(DEV_TEST_DB_DSN)" PYTHONPATH=.
TEST_ENV := D2C_BACKOFFICE_ENVIRONMENT=test D2C_BACKOFFICE_DATABASE_URL="$(DEV_TEST_DB_DSN)" D2C_BACKOFFICE_TEST_DATABASE_URL="$(DEV_TEST_DB_DSN)" PYTHONPATH=.
PMS_SYNC_ENV := $(DEV_ENV) D2C_BACKOFFICE_PMS_API_BASE_URL="$(PMS_API_BASE_URL)" D2C_BACKOFFICE_PMS_SERVICE_CLIENT_CODE="$(PMS_SERVICE_CLIENT_CODE)" D2C_BACKOFFICE_PMS_PROJECTION_SYNC_PAGE_LIMIT="$(PMS_PROJECTION_SYNC_PAGE_LIMIT)"

TESTS ?= tests
PYTEST_ARGS ?=

.PHONY: clean-pyc install lint test routes openapi check
.PHONY: upgrade-dev alembic-check alembic-current alembic-history revision
.PHONY: pms-projection-sync pms-projection-sync-products pms-projection-sync-units
.PHONY: pms-projection-sync-sku-codes pms-projection-sync-barcodes
.PHONY: uvicorn uvicorn-up uvicorn-down uvicorn-restart uvicorn-status uvicorn-logs
.PHONY: up down restart status logs

clean-pyc:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

install:
	$(PYTHON) -m venv .venv
	$(VENV_PYTHON) -m pip install -U pip
	$(VENV_PYTHON) -m pip install -e ".[dev]"

lint: clean-pyc
	$(VENV_PYTHON) -m ruff check app tests scripts alembic

test: clean-pyc
	$(TEST_ENV) $(VENV_PYTHON) -m pytest $(TESTS) $(PYTEST_ARGS)

routes:
	PYTHONPATH=. $(VENV_PYTHON) scripts/list_routes.py

openapi:
	PYTHONPATH=. $(VENV_PYTHON) scripts/export_openapi.py

check: lint test routes openapi

upgrade-dev:
	$(DEV_ENV) $(VENV_PYTHON) -m alembic upgrade head

alembic-check:
	$(DEV_ENV) $(VENV_PYTHON) -m alembic check

alembic-current:
	$(DEV_ENV) $(VENV_PYTHON) -m alembic current

alembic-history:
	$(DEV_ENV) $(VENV_PYTHON) -m alembic history

revision:
	$(DEV_ENV) $(VENV_PYTHON) -m alembic revision --autogenerate -m "$(MSG)"

pms-projection-sync: clean-pyc
	$(PMS_SYNC_ENV) $(VENV_PYTHON) scripts/sync_pms_projection.py --scope all --requested-by "$(PMS_PROJECTION_SYNC_REQUESTED_BY)"

pms-projection-sync-products: clean-pyc
	$(PMS_SYNC_ENV) $(VENV_PYTHON) scripts/sync_pms_projection.py --scope products --requested-by "$(PMS_PROJECTION_SYNC_REQUESTED_BY)"

pms-projection-sync-units: clean-pyc
	$(PMS_SYNC_ENV) $(VENV_PYTHON) scripts/sync_pms_projection.py --scope units --requested-by "$(PMS_PROJECTION_SYNC_REQUESTED_BY)"

pms-projection-sync-sku-codes: clean-pyc
	$(PMS_SYNC_ENV) $(VENV_PYTHON) scripts/sync_pms_projection.py --scope sku_codes --requested-by "$(PMS_PROJECTION_SYNC_REQUESTED_BY)"

pms-projection-sync-barcodes: clean-pyc
	$(PMS_SYNC_ENV) $(VENV_PYTHON) scripts/sync_pms_projection.py --scope barcodes --requested-by "$(PMS_PROJECTION_SYNC_REQUESTED_BY)"

uvicorn:
	PYTHONPATH=. $(VENV_PYTHON) -m uvicorn app.main:app --host $(HOST) --port $(PORT)

uvicorn-up:
	@if [ -f "$(PID_FILE)" ] && kill -0 "$$(cat $(PID_FILE))" 2>/dev/null; then \
	  echo "d2c-backoffice-api already running: $(HEALTH_URL)"; \
	else \
	  echo "starting d2c-backoffice-api on $(HOST):$(PORT)"; \
	  nohup env PYTHONPATH=. D2C_BACKOFFICE_API_PORT="$(PORT)" D2C_BACKOFFICE_DATABASE_URL="$(DEV_DB_DSN)" \
	    $(VENV_PYTHON) -m uvicorn app.main:app --host $(HOST) --port $(PORT) >"$(LOG_FILE)" 2>&1 & \
	  echo $$! > "$(PID_FILE)"; \
	  for i in 1 2 3 4 5 6 7 8 9 10; do \
	    if curl -fsS "$(HEALTH_URL)" >/dev/null 2>&1; then \
	      echo "d2c-backoffice-api ready: $(HEALTH_URL)"; \
	      break; \
	    fi; \
	    echo "waiting d2c-backoffice-api attempt $$i"; \
	    sleep 1; \
	  done; \
	fi

uvicorn-down:
	@if [ -f "$(PID_FILE)" ]; then \
	  OLD_PID="$$(cat $(PID_FILE))"; \
	  echo "stopping d2c-backoffice-api pid: $$OLD_PID"; \
	  kill "$$OLD_PID" 2>/dev/null || true; \
	  for i in 1 2 3 4 5; do \
	    if kill -0 "$$OLD_PID" 2>/dev/null; then \
	      sleep 1; \
	    else \
	      break; \
	    fi; \
	  done; \
	  if kill -0 "$$OLD_PID" 2>/dev/null; then \
	    echo "force stopping d2c-backoffice-api pid: $$OLD_PID"; \
	    kill -9 "$$OLD_PID" 2>/dev/null || true; \
	  fi; \
	  rm -f "$(PID_FILE)"; \
	fi
	@echo "d2c-backoffice-api stopped if it was running"

uvicorn-restart: uvicorn-down uvicorn-up

uvicorn-status:
	@if [ -f "$(PID_FILE)" ] && kill -0 "$$(cat $(PID_FILE))" 2>/dev/null; then \
	  echo "running pid=$$(cat $(PID_FILE))"; \
	  curl -fsS "$(HEALTH_URL)" || true; \
	else \
	  echo "not running"; \
	fi

uvicorn-logs:
	@if [ -f "$(LOG_FILE)" ]; then \
	  tail -n 120 "$(LOG_FILE)"; \
	else \
	  echo "no log file: $(LOG_FILE)"; \
	fi

up: uvicorn-up
down: uvicorn-down
restart: uvicorn-restart
status: uvicorn-status
logs: uvicorn-logs
