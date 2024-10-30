data_model_dict = {
    "nodes": [
        {
            "label": "NodeA",
            "properties": [
                {
                    "name": "prop1",
                    "type": "str",
                    "column_mapping": "prop_1",
                    "is_unique": True,
                },
                {
                    "name": "prop2",
                    "type": "int",
                    "column_mapping": "prop_2",
                    "is_unique": False,
                },
                {
                    "name": "prop3",
                    "type": "float",
                    "column_mapping": "prop_3",
                    "is_unique": False,
                },
            ],
        },
        {
            "label": "NodeB",
            "properties": [
                {
                    "name": "prop4",
                    "type": "str",
                    "column_mapping": "prop_4",
                    "is_unique": True,
                },
                {
                    "name": "prop5",
                    "type": "int",
                    "column_mapping": "prop_5",
                    "is_unique": False,
                },
                {
                    "name": "prop6",
                    "type": "float",
                    "column_mapping": "prop_6",
                    "is_unique": False,
                },
            ],
        },
    ],
    "relationships": [
        {
            "type": "RELATIONSHIP_AB",
            "properties": [
                {
                    "name": "prop7",
                    "type": "float",
                    "column_mapping": "prop_7",
                    "is_unique": False,
                }
            ],
            "source": "NodeA",
            "target": "NodeB",
        }
    ],
}

data_model_yaml = """nodes:
- file_name: file
  label: NodeA
  properties:
  - alias: null
    column_mapping: prop_1
    is_unique: true
    name: prop1
    part_of_key: false
    type: str
  - alias: null
    column_mapping: prop_2
    is_unique: false
    name: prop2
    part_of_key: false
    type: int
  - alias: null
    column_mapping: prop_3
    is_unique: false
    name: prop3
    part_of_key: false
    type: float
- file_name: file
  label: NodeB
  properties:
  - alias: null
    column_mapping: prop_4
    is_unique: true
    name: prop4
    part_of_key: false
    type: str
  - alias: null
    column_mapping: prop_5
    is_unique: false
    name: prop5
    part_of_key: false
    type: int
  - alias: null
    column_mapping: prop_6
    is_unique: false
    name: prop6
    part_of_key: false
    type: float
relationships:
- file_name: file
  properties:
  - alias: null
    column_mapping: prop_7
    is_unique: false
    name: prop7
    part_of_key: false
    type: float
  source: NodeA
  target: NodeB
  type: RELATIONSHIP_AB
"""
