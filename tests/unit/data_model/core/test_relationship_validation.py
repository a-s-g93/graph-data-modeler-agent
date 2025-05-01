from typing import Any, Dict

import pytest
from pydantic import ValidationError

from graph_data_modeler_agent.data_model.core import Relationship
from graph_data_modeler_agent.exceptions import InvalidSourceNameError


@pytest.fixture(scope="function")
def relationship_validation_context() -> Dict[str, Any]:
    return {
        "valid_sources": ["a.csv", "b.csv"],
        "enforce_uniqueness": True,
        "valid_columns": {"a.csv": ["nkey"], "b.csv": ["col"]},
    }


def test_validate_wrong_source_file_name_multifile(
    relationship_validation_context: Dict[str, Any], relationship_data: Dict[str, Any]
) -> None:
    relationship_data["source_name"] = "wrong.csv"
    with pytest.raises(ValidationError) as e:
        Relationship.model_validate(relationship_data, context=relationship_validation_context)
    
    # Verify the error message mentions the invalid source name
    assert "wrong.csv is not in the provided file list" in str(e.value)


def test_validate_wrong_source_file_name_singlefile(
    relationship_data: Dict[str, Any],
) -> None:
    assert relationship_data.get("source_name") == "a.csv"
    relationship = Relationship.model_validate(
        relationship_data, context={"valid_sources": ["b.csv"], "valid_columns": {"b.csv": ["nkey"]}}
    )
    assert relationship.source_name == "b.csv"


def test_enforce_uniqueness_pass(
    relationship_context: Dict[str, Any], relationship_data: Dict[str, Any]
) -> None:
    assert relationship_context.get("enforce_uniqueness")
    Relationship.model_validate(relationship_data, context=relationship_context)


# Don't enforce relationship uniqueness feature at this time.
# def test_enforce_uniqueness_fail(relationship_context: Dict[str, Any], relationship_data: Dict[str, Any]) -> None:

#     data = relationship_data
#     data.get("properties")[0]["is_unique"] = False

#     with pytest.raises(ValidationError):
#         Relationship.model_validate(data, context=relationship_context)


def test_validate_property_mappings_one_prop(
    relationship_validation_context: Dict[str, Any], relationship_data: Dict[str, Any]
) -> None:
    relationship_data["properties"] = [
        {
            "name": "nkey",
            "type": "STRING",
            "column_mapping": "wrong",
            "is_key": True,
        }
    ]
    relationship_validation_context["table_column_listings"] = {"a.csv": ["nkey"], "b.csv": ["col"]}
    
    with pytest.raises(ValidationError):
        Relationship.model_validate(relationship_data, context=relationship_validation_context)


def test_validate_property_mappings_two_props(
    relationship_validation_context: Dict[str, Any], relationship_data: Dict[str, Any]
) -> None:
    relationship_data["properties"] = [
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
    relationship_validation_context["table_column_listings"] = {"a.csv": ["nkey"], "b.csv": ["col"]}
    
    with pytest.raises(ValidationError) as e:
        Relationship.model_validate(relationship_data, context=relationship_validation_context)
    assert "wrong1" in str(e.value)
    assert "wrong2" in str(e.value)


def test_missing_valid_columns_context(
    relationship_data: Dict[str, Any], relationship_context: Dict[str, Any]
) -> None:
    del relationship_context["valid_columns"]
    Relationship.model_validate(relationship_data, context=relationship_context)


def test_no_context(relationship_data: Dict[str, Any]) -> None:
    Relationship.model_validate(relationship_data)


def test_no_context_standard_init(relationship_data: Dict[str, Any]) -> None:
    Relationship(**relationship_data)
