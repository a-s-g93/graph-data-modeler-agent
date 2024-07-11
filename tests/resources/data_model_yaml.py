data_model_dict = {
    "nodes": [
        {
            "label": "NodeA",
            "properties": [
                {
                    "name": "prop1",
                    "type": "str",
                    "csv_mapping": "prop_1",
                    "is_unique": True,
                },
                {
                    "name": "prop2",
                    "type": "int",
                    "csv_mapping": "prop_2",
                    "is_unique": False,
                },
                {
                    "name": "prop3",
                    "type": "float",
                    "csv_mapping": "prop_3",
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
                    "csv_mapping": "prop_4",
                    "is_unique": True,
                },
                {
                    "name": "prop5",
                    "type": "int",
                    "csv_mapping": "prop_5",
                    "is_unique": False,
                },
                {
                    "name": "prop6",
                    "type": "float",
                    "csv_mapping": "prop_6",
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
                    "csv_mapping": "prop_7",
                    "is_unique": False,
                }
            ],
            "source": "NodeA",
            "target": "NodeB",
        }
    ],
}

data_model_yaml = """nodes:
- csv_name: ''
  label: NodeA
  properties:
  - csv_mapping: prop_1
    csv_mapping_other: null
    is_unique: true
    name: prop1
    part_of_key: false
    type: str
  - csv_mapping: prop_2
    csv_mapping_other: null
    is_unique: false
    name: prop2
    part_of_key: false
    type: int
  - csv_mapping: prop_3
    csv_mapping_other: null
    is_unique: false
    name: prop3
    part_of_key: false
    type: float
- csv_name: ''
  label: NodeB
  properties:
  - csv_mapping: prop_4
    csv_mapping_other: null
    is_unique: true
    name: prop4
    part_of_key: false
    type: str
  - csv_mapping: prop_5
    csv_mapping_other: null
    is_unique: false
    name: prop5
    part_of_key: false
    type: int
  - csv_mapping: prop_6
    csv_mapping_other: null
    is_unique: false
    name: prop6
    part_of_key: false
    type: float
relationships:
- csv_name: ''
  properties:
  - csv_mapping: prop_7
    csv_mapping_other: null
    is_unique: false
    name: prop7
    part_of_key: false
    type: float
  source: NodeA
  target: NodeB
  type: RELATIONSHIP_AB
"""
