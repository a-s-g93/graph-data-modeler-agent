from graph_data_modeler_agent.data_model.core import Property

def test_property_name_formatting() -> None:
    """Should format property names based on Neo4j naming conventions"""

    p = Property(
        name="test_property", type="STRING", column_mapping="col1", is_key=False
    )

    assert p.name == "testProperty"  # Should be camelCase per Neo4j conventions

def test_property_type_validation() -> None:
    """Test type validation and conversion"""
    
    # Test string type conversion
    p1 = Property(
        name="test", type="string", column_mapping="col1", is_key=False
    )
    assert p1.type == "STRING"
    
    # Test integer type conversion
    p2 = Property(
        name="test", type="int", column_mapping="col1", is_key=False
    )
    assert p2.type == "INTEGER"
    
    # Test float type conversion
    p3 = Property(
        name="test", type="float64", column_mapping="col1", is_key=False
    )
    assert p3.type == "FLOAT"
    
    # Test boolean type conversion
    p4 = Property(
        name="test", type="boolean", column_mapping="col1", is_key=False
    )
    assert p4.type == "BOOLEAN"
