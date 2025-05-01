from typing import Any, Dict, Iterator, List

import pytest
from pydantic import ValidationError

from graph_data_modeler_agent.data_model.core import DataModel
from graph_data_modeler_agent.exceptions import InvalidSourceNameError


@pytest.fixture(scope="function")
def data_model_validation_context() -> Dict[str, Any]:
    return {
        "valid_sources": ["a.csv", "b.csv"],
        "enforce_uniqueness": True,
        "valid_columns": {"a.csv": ["nkey"], "b.csv": ["col"]},
    }


def test_validate_wrong_source_file_name_multifile(
    data_model_validation_context: Dict[str, Any], data_model_data: Dict[str, Any]
) -> None:
    data_model_data["nodes"][0]["source_name"] = "wrong.csv"
    with pytest.raises(ValidationError) as e:
        DataModel.model_validate(data_model_data, context=data_model_validation_context)
    
    # Verify the error message mentions the invalid source name
    assert "wrong.csv is not in the provided file list" in str(e.value)


def test_validate_wrong_source_file_name_singlefile(
    data_model_data: Dict[str, Any],
) -> None:
    assert data_model_data.get("nodes")[0]["source_name"] == "a.csv"
    
    # Include all necessary columns in valid_columns for b.csv
    columns_needed = ["id", "b", "c", "col"]
    
    dm = DataModel.model_validate(
        data_model_data, 
        context={
            "valid_sources": ["b.csv"], 
            "valid_columns": {"b.csv": columns_needed},
            "allow_duplicate_column_mappings": True  # Allow duplicate column mappings
        }
    )
    assert dm.nodes[0].source_name == "b.csv"


def test_validate_property_mappings_one_prop(
    data_model_validation_context: Dict[str, Any], data_model_data: Dict[str, Any]
) -> None:
    data_model_data["nodes"][0]["properties"] = [
        {
            "name": "nkey",
            "type": "STRING",
            "column_mapping": "wrong",
            "is_key": True,
        }
    ]
    data_model_validation_context["table_column_listings"] = {"a.csv": ["nkey"], "b.csv": ["col"]}
    
    with pytest.raises(ValidationError):
        DataModel.model_validate(data_model_data, context=data_model_validation_context)


def test_missing_valid_columns_context(
    data_model_data: Dict[str, Any], data_model_context: Dict[str, Any]
) -> None:
    del data_model_context["valid_columns"]
    DataModel.model_validate(data_model_data, context=data_model_context)


def test_no_context(data_model_data: Dict[str, Any]) -> None:
    DataModel.model_validate(data_model_data)


def test_no_context_standard_init(data_model_data: Dict[str, Any]) -> None:
    DataModel(**data_model_data)


def test_multi_file_different_source_relationship_valid_source_node(
    data_model_data: Dict[str, Any], data_model_context: Dict[str, Any]
) -> None:
    DataModel.model_validate(data_model_data, context=data_model_context)


def test_multi_file_different_source_relationship_valid_target_node(
    data_model_flipped_data: Dict[str, Any], data_model_context: Dict[str, Any]
) -> None:
    DataModel.model_validate(data_model_flipped_data, context=data_model_context)


def test_multi_file_different_source_relationship_invalid(
    data_model_data: Dict[str, Any], data_model_bad_context: Dict[str, Any]
) -> None:
    with pytest.raises(ValidationError) as e:
        DataModel.model_validate(data_model_data, context=data_model_bad_context)

    assert (
        "relationship_source_file_missing_source_node_unique_property_alias_error"
        in str(e.value)
    )


def test_allow_duplicate_properties_true(
    data_model_dupe_prop_data: Dict[str, Any], data_model_context: Dict[str, Any]
) -> None:
    data_model_context["allow_duplicate_column_mappings"] = True

    DataModel.model_validate(data_model_dupe_prop_data, context=data_model_context)


def test_allow_duplicate_properties_false(
    data_model_dupe_prop_data: Dict[str, Any], data_model_context: Dict[str, Any]
) -> None:
    with pytest.raises(ValidationError) as e:
        DataModel.model_validate(data_model_dupe_prop_data, context=data_model_context)

    assert "duplicate_property_in_data_model_error" in str(e.value)


def test_node_field_validator_error(
    data_model_data: Dict[str, Any], data_model_context: Dict[str, Any]
) -> None:
    data_model_data["nodes"][0]["source_name"] = "wrongfile.csv"

    with pytest.raises(ValidationError) as e:
        DataModel.model_validate(data_model_data, context=data_model_context)

    # Check for column mapping error with wrongfile.csv
    assert "not allowed for source file wrongfile.csv" in str(e.value)


def test_node_model_validator_error(
    data_model_data: Dict[str, Any], data_model_context: Dict[str, Any]
) -> None:
    data_model_data["nodes"][0]["properties"] = [
        {
            "name": "nkey",
            "type": "STRING",
            "column_mapping": "wrong_mapping",
            "is_key": True,
        }
    ]
    with pytest.raises(ValueError) as e:
        DataModel.model_validate(data_model_data, context=data_model_context)

    assert "invalid_column_mapping_error" in str(e.value)


def test_relationship_field_validator_error(
    data_model_data: Dict[str, Any], data_model_context: Dict[str, Any]
) -> None:
    # First ensure a valid context without data_dictionary to avoid KeyError
    if "data_dictionary" in data_model_context:
        del data_model_context["data_dictionary"]
    
    # Set an invalid source_name
    data_model_data["relationships"][0]["source_name"] = "wrongfile.csv"
    
    # Ensure valid_sources is in the context to trigger validation
    if "valid_sources" not in data_model_context:
        data_model_context["valid_sources"] = ["a.csv", "b.csv"]

    with pytest.raises(ValidationError) as e:
        DataModel.model_validate(data_model_data, context=data_model_context)

    # Check for error with wrongfile.csv
    assert "wrongfile.csv" in str(e.value)


def test_relationship_model_validator_error(
    data_model_data: Dict[str, Any], data_model_context: Dict[str, Any]
) -> None:
    data_model_data["relationships"][0]["properties"] = [
        {
            "name": "nkey",
            "type": "STRING",
            "column_mapping": "wrong_mapping",
            "is_key": False,
        }
    ]
    with pytest.raises(ValueError) as e:
        DataModel.model_validate(data_model_data, context=data_model_context)

    assert "invalid_column_mapping_error" in str(e.value)


def test_node_property_field_validator_error(
    data_model_data: Dict[str, Any], data_model_context: Dict[str, Any]
) -> None:
    data_model_data["relationships"][0]["properties"] = [
        {
            "name": "nkey",
            "type": "wrong_type",
            "column_mapping": "nkey",
            "is_key": False,
        }
    ]
    with pytest.raises(ValueError) as e:
        DataModel.model_validate(data_model_data, context=data_model_context)

    assert "Invalid Property type given: wrong_type" in str(e.value)


def test_allow_parallel_relationships_same_direction(
    data_model_parallel_data: Dict[str, Any],
    data_model_parallel_context: Dict[str, Any],
) -> None:
    with pytest.raises(ValidationError) as e:
        DataModel.model_validate(
            data_model_parallel_data, context=data_model_parallel_context
        )

    assert "parallel_relationship_error" in str(e.value)


def test_allow_parallel_relationships_opposite_direction(
    data_model_parallel_data: Dict[str, Any],
    data_model_parallel_context: Dict[str, Any],
) -> None:
    data_model_parallel_data["relationships"][0]["source"] = "LabelB"
    data_model_parallel_data["relationships"][0]["target"] = "LabelA"

    with pytest.raises(ValidationError) as e:
        DataModel.model_validate(
            data_model_parallel_data, context=data_model_parallel_context
        )

    assert "parallel_relationship_error" in str(e.value)


def test_ignore_parallel_relationships(
    data_model_parallel_data: Dict[str, Any],
    data_model_parallel_context: Dict[str, Any],
) -> None:
    data_model_parallel_context["allow_parallel_relationships"] = True

    DataModel.model_validate(
        data_model_parallel_data, context=data_model_parallel_context
    )
