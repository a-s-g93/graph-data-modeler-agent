from typing import Any, Dict

import pytest
from pydantic import ValidationError

from graph_data_modeler_agent.data_model.core import Node
from graph_data_modeler_agent.exceptions import InvalidSourceNameError


@pytest.fixture(scope="function")
def node_validation_context() -> Dict[str, Any]:
    return {
        "valid_sources": ["a.csv", "b.csv"],
        "enforce_uniqueness": True,
        "valid_columns": {"a.csv": ["nkey"], "b.csv": ["col"]},
    }


def test_validate_wrong_source_file_name_multifile(
    node_validation_context: Dict[str, Any], node_data: Dict[str, Any]
) -> None:
    node_data["source_name"] = "wrong.csv"
    with pytest.raises(ValidationError) as e:
        Node.model_validate(node_data, context=node_validation_context)
    
    # Verify the error message mentions the invalid source name
    assert "wrong.csv is not in the provided file list" in str(e.value)


def test_validate_wrong_source_file_name_singlefile(node_data: Dict[str, Any]) -> None:
    assert node_data.get("source_name") == "a.csv"
    node = Node.model_validate(
        node_data, context={"valid_sources": ["b.csv"], "valid_columns": {"b.csv": ["nkey"]}}
    )
    assert node.source_name == "b.csv"


def test_enforce_uniqueness_pass(
    node_context: Dict[str, Any], node_data: Dict[str, Any]
) -> None:
    assert node_context.get("enforce_uniqueness")
    Node.model_validate(node_data, context=node_context)


def test_enforce_uniqueness_fail(
    node_context: Dict[str, Any], node_data: Dict[str, Any]
) -> None:
    data = node_data
    data.get("properties")[0]["is_key"] = False

    with pytest.raises(ValidationError):
        Node.model_validate(data, context=node_context)


def test_validate_property_mappings_one_prop(
    node_validation_context: Dict[str, Any], node_data: Dict[str, Any]
) -> None:
    node_data["properties"] = [
        {
            "name": "nkey",
            "type": "STRING",
            "column_mapping": "wrong",
            "is_key": True,
        }
    ]
    node_validation_context["table_column_listings"] = {"a.csv": ["nkey"], "b.csv": ["col"]}
    
    with pytest.raises(ValidationError):
        Node.model_validate(node_data, context=node_validation_context)


def test_validate_property_mappings_two_props(
    node_validation_context: Dict[str, Any], node_data: Dict[str, Any]
) -> None:
    node_data["properties"] = [
        {
            "name": "nkey",
            "type": "STRING",
            "column_mapping": "wrong1",
            "is_key": True,
        },
        {
            "name": "nkey2",
            "type": "STRING",
            "column_mapping": "wrong2",
            "is_key": True,
        }
    ]
    node_validation_context["table_column_listings"] = {"a.csv": ["nkey"], "b.csv": ["col"]}
    
    with pytest.raises(ValidationError) as e:
        Node.model_validate(node_data, context=node_validation_context)
    assert "wrong1" in str(e.value)
    assert "wrong2" in str(e.value)


def test_wrong_source_file_and_wrong_attr_type(
    node_validation_context: Dict[str, Any], node_data: Dict[str, Any]
) -> None:
    node_data["source_name"] = "wrong.csv"
    node_data["properties"] = [
        {
            "name": "nkey",
            "type": "STRING",
            "column_mapping": "nkey",
            "is_key": "3",  # Invalid boolean value
        }
    ]

    with pytest.raises(ValidationError) as e:
        Node.model_validate(node_data, context=node_validation_context)

    assert "Input should be a valid boolean" in str(e.value)


def test_missing_enforce_uniqueness_context(
    node_context: Dict[str, Any], node_data: Dict[str, Any]
) -> None:
    del node_context["enforce_uniqueness"]
    Node.model_validate(node_data, context=node_context)


def test_missing_valid_columns_context(
    node_context: Dict[str, Any], node_data: Dict[str, Any]
) -> None:
    del node_context["valid_columns"]
    Node.model_validate(node_data, context=node_context)


def test_no_context(node_data: Dict[str, Any]) -> None:
    Node.model_validate(node_data)


def test_no_context_standard_init(node_data: Dict[str, Any]) -> None:
    Node(**node_data)
