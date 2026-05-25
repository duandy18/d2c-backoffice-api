from sqlalchemy import inspect

from app.core.config import load_settings
from app.core.database import create_engine


def test_client_presentation_protocol_owner_and_snapshot_tables_exist() -> None:
    engine = create_engine(load_settings().database_url)
    try:
        table_names = set(inspect(engine).get_table_names())

        assert {
            "d2c_client_surfaces",
            "d2c_client_data_bindings",
            "d2c_client_visibility_rules",
            "d2c_client_action_policies",
            "d2c_client_tracking_policies",
            "d2c_published_client_surfaces",
            "d2c_published_client_data_bindings",
            "d2c_published_client_visibility_rules",
            "d2c_published_client_action_policies",
            "d2c_published_client_tracking_policies",
        }.issubset(table_names)
    finally:
        engine.dispose()


def test_client_presentation_protocol_owner_columns_exist() -> None:
    engine = create_engine(load_settings().database_url)
    try:
        inspector = inspect(engine)

        surface_columns = {
            column["name"] for column in inspector.get_columns("d2c_client_surfaces")
        }
        binding_columns = {
            column["name"] for column in inspector.get_columns("d2c_client_data_bindings")
        }
        visibility_columns = {
            column["name"] for column in inspector.get_columns("d2c_client_visibility_rules")
        }
        action_columns = {
            column["name"] for column in inspector.get_columns("d2c_client_action_policies")
        }
        tracking_columns = {
            column["name"] for column in inspector.get_columns("d2c_client_tracking_policies")
        }

        assert {"surface_code", "device_family", "supported_renderer_keys"}.issubset(
            surface_columns
        )
        assert {"binding_code", "data_source_type", "query_params", "result_limit"}.issubset(
            binding_columns
        )
        assert {"rule_code", "client_surface_codes", "rule_expression", "priority"}.issubset(
            visibility_columns
        )
        assert {"policy_code", "action_type", "target_page_code", "action_payload"}.issubset(
            action_columns
        )
        assert {"policy_code", "event_name", "event_trigger", "tracking_params"}.issubset(
            tracking_columns
        )
    finally:
        engine.dispose()
