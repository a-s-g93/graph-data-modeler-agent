import pytest
from pydantic import ValidationError

from graph_data_modeler_agent.data_model.core import DataModel, Node, Property, Relationship
from tests.resources.answers.data_model_yaml import data_model_dict, data_model_yaml

columns = [
    "name",
    "age",
    "street",
    "city",
    "pet_name",
    "pet",
    "toy",
    "toy_type",
]

person_name = Property(
    name="name", type="STRING", column_mapping="name", is_key=True, alias="knows"
)
person_age = Property(name="age", type="STRING", column_mapping="age", is_key=False)
address_street = Property(
    name="street",
    type="STRING",
    column_mapping="street",
    is_key=True,
)
address_city = Property(
    name="city", type="STRING", column_mapping="city", is_key=False,
)
pet_name = Property(name="name", type="STRING", column_mapping="pet_name", is_key=True)
pet_kind = Property(name="kind", type="STRING", column_mapping="pet", is_key=False)
toy_name = Property(name="name", type="STRING", column_mapping="toy", is_key=True)
toy_kind = Property(name="kind", type="STRING", column_mapping="toy_type", is_key=False)

good_nodes = [
    Node(
        label="Person",
        properties=[person_name, person_age],
        source_name="people_pets.csv",
    ),
    Node(
        label="Address",
        properties=[address_street, address_city],
         source_name="people_pets.csv",
    ),
    Node(
        label="Pet",
        properties=[pet_name, pet_kind],
        source_name="people_pets.csv",
    ),
    Node(
        label="Toy",
        properties=[toy_name, toy_kind],
        source_name="people_pets.csv",
    ),
]

good_relationships = [
    Relationship(
        type="HAS_ADDRESS",
        properties=[],
        source="Person",
        target="Address",
        source_name="people_pets.csv",
    ),
    Relationship(
        type="KNOWS",
        properties=[],
        source="Person",
        target="Person",
        source_name="people_pets.csv",
    ),
    Relationship(
        type="HAS_PET",
        properties=[],
        source="Person",
        target="Pet",
        source_name="people_pets.csv",
    ),
    Relationship(
        type="PLAYS_WITH",
        properties=[],
        source="Pet",
        target="Toy",
        source_name="people_pets.csv",
    ),
]
bad_relationships = good_relationships + [
    Relationship(
        type="BAD",
        properties=[],
        source="Dog",
        target="Toy",
        source_name="people_pets.csv",
    )
]
bad_nodes = good_nodes + [
    Node(
        label="Toy",
        properties=[toy_name, toy_kind],
        source_name="people_pets.csv",
    )
]


def test_bad_init() -> None:
    """
    Test bad input for init.
    """

    with pytest.raises(ValidationError) as e:
        DataModel(nodes=bad_nodes, relationships=bad_relationships)


def test_good_init() -> None:
    """
    This input should pass.
    """

    # valid
    assert isinstance(
        DataModel(nodes=good_nodes, relationships=good_relationships),
        DataModel,
    )


def test_to_dict() -> None:
    """
    Test model_dump property.
    """

    test_model = DataModel(nodes=good_nodes, relationships=good_relationships)

    test_dict = test_model.model_dump()

    assert list(test_dict.keys()) == ["nodes", "relationships", "metadata"]
    assert list(test_dict["nodes"][0].keys()) == ["label", "properties", "source_name"]
    assert list(test_dict["relationships"][0].keys()) == [
        "type",
        "properties",
        "source",
        "target",
        "source_name",
    ]


def test_neo4j_naming_conventions_used() -> None:
    """
    Test renaming labels, types and properties to Neo4j naming conventions.
    """

    prop1 = {
        "name": "Name",
        "type": "STRING",
        "column_mapping": "name",
        "alias": "knows_person",
        "is_key": True,
    }
    prop2 = {
        "name": "person_age",
        "type": "INTEGER",
        "column_mapping": "age",
        "is_key": False,
    }
    prop3 = {
        "name": "CurrentStreet",
        "type": "STRING",
        "column_mapping": "street",
        "is_key": True,
    }
    prop4 = {
        "name": "favorite_score",
        "type": "INTEGER",
        "column_mapping": "favorite",
        "is_key": False,
    }

    name_conv_nodes = [
        {
            "label": "person",
            "properties": [prop1, prop2],
            "source_name": "people.csv",
        },
        {
            "label": "current_Address",
            "properties": [prop3],
            "source_name": "addresses.csv",
        },
    ]

    name_conv_relationships = [
        {
            "type": "has_address",
            "properties": [prop4],
            "source": "Person",
            "target": "current_address",
        },
        {
            "type": "HasSecondAddress",
            "source": "person",
            "target": "current_Address",
        },
        {
            "type": "hasAddress_Three",
            "source": "Person",
            "target": "CurrentAddress",
        },
    ]

    dm = DataModel.model_validate(
        {"nodes": name_conv_nodes, "relationships": name_conv_relationships},
        context={"allow_parallel_relationships": True},
    )

    assert set(dm.node_labels) == {"Person", "CurrentAddress"}
    assert set(dm.relationship_types) == {
        "HAS_ADDRESS",
        "HAS_SECOND_ADDRESS",
        "HAS_ADDRESS_THREE",
    }

    for rel in dm.relationships:
        assert rel.source in ["Person", "CurrentAddress"]
        assert rel.target in ["Person", "CurrentAddress"]


def test_neo4j_naming_conventions_ignored() -> None:
    prop1 = {
        "name": "Name",
        "type": "STRING",
        "column_mapping": "name",
        "alias": "knows_person",
        "is_key": True,
    }

    prop3 = {
        "name": "CurrentStreet",
        "type": "STRING",
        "column_mapping": "street",
        "is_key": True,
    }

    name_conv_nodes = [
        {
            "label": "person",
            "properties": [prop1],
            "source_name": "people_pets.csv",
        },
        {
            "label": "current_address",
            "properties": [prop3],
            "source_name": "people_pets.csv",
        },
    ]

    name_conv_relationships = [
        {
            "type": "has_address",
            "source": "person",
            "target": "current_address",
        }
    ]

    dm = DataModel.model_validate(
        {"nodes": name_conv_nodes, "relationships": name_conv_relationships},
        context={"apply_neo4j_naming_conventions": False},
    )

    assert set(dm.node_labels) == {"person", "current_address"}
    assert set(dm.relationship_types) == {"has_address"}

    for rel in dm.relationships:
        assert rel.source in ["person", "current_address"]
        assert rel.target in ["person", "current_address"]


def test_from_arrows_init() -> None:
    """
    Test init from arrows json file.
    """

    data_model = DataModel.from_arrows(
        file_path="tests/resources/data_models/arrows-data-model.json"
    )

    assert data_model.nodes[0].properties[0].is_key
    assert data_model.nodes[0].properties[1].type == "INTEGER"
    assert data_model.nodes[0].label == "Person"


def test_to_yaml_string() -> None:
    """
    Test data model output to yaml format string.
    """

    data_model = DataModel.model_validate(
        {"nodes": data_model_dict["nodes"], "relationships": data_model_dict["relationships"]},
        context={"enforce_uniqueness": False, "apply_neo4j_naming_conventions": False}
    )

    # Get the YAML output
    yaml_output = data_model.to_yaml(write_file=False)
    
    # Check that the YAML contains expected structure
    assert "nodes:" in yaml_output
    assert "label:" in yaml_output
    assert "properties:" in yaml_output
    assert "column_mapping:" in yaml_output
    assert "is_key:" in yaml_output
    assert "name:" in yaml_output
    assert "type:" in yaml_output
    assert "source_name:" in yaml_output
    assert "relationships:" in yaml_output
    assert "source:" in yaml_output
    assert "target:" in yaml_output
    assert "RELATIONSHIP_AB" in yaml_output


def test_data_model_with_multi_csv_from_arrows() -> None:
    data_model = DataModel.from_arrows(
        "tests/resources/data_models/people-pets-arrows-multi-csv.json"
    )

    assert data_model.relationships[-1].source_name == "shelters.csv"
    assert data_model.relationships[0].source_name == "pets-arrows.csv"
    assert data_model.nodes[0].source_name == "pets-arrows.csv"


def test_data_model_with_multi_csv_from_solutions_workbench() -> None:
    pass
