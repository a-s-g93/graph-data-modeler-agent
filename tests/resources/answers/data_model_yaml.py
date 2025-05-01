data_model_dict = {
    "nodes": [
        {
            "label": "NodeA",
            "properties": [
                {
                    "name": "prop1",
                    "type": "STRING",
                    "column_mapping": "prop_1",
                    "is_key": True,
                },
                {
                    "name": "prop2",
                    "type": "INTEGER",
                    "column_mapping": "prop_2",
                    "is_key": False,
                },
                {
                    "name": "prop3",
                    "type": "FLOAT",
                    "column_mapping": "prop_3",
                    "is_key": False,
                },
            ],
            "source_name": "file.csv",
        },
        {
            "label": "NodeB",
            "properties": [
                {
                    "name": "prop4",
                    "type": "STRING",
                    "column_mapping": "prop_4",
                    "is_key": True,
                },
                {
                    "name": "prop5",
                    "type": "INTEGER",
                    "column_mapping": "prop_5",
                    "is_key": False,
                },
                {
                    "name": "prop6",
                    "type": "FLOAT",
                    "column_mapping": "prop_6",
                    "is_key": False,
                },
            ],
            "source_name": "file.csv",
        },
    ],
    "relationships": [
        {
            "type": "RELATIONSHIP_AB",
            "properties": [
                {
                    "name": "prop7",
                    "type": "FLOAT",
                    "column_mapping": "prop_7",
                    "is_key": False,
                }
            ],
            "source": "NodeA",
            "target": "NodeB",
        }
    ],
}

data_model_yaml = """nodes:
- label: NodeA
  properties:
  - alias: null
    column_mapping: prop_1
    is_key: true
    name: prop1
    part_of_key: false
    type: STRING
  - alias: null
    column_mapping: prop_2
    is_key: false
    name: prop2
    part_of_key: false
    type: INTEGER
  - alias: null
    column_mapping: prop_3
    is_key: false
    name: prop3
    part_of_key: false
    type: FLOAT
  source_name: file.csv
- label: NodeB
  properties:
  - alias: null
    column_mapping: prop_4
    is_key: true
    name: prop4
    part_of_key: false
    type: STRING
  - alias: null
    column_mapping: prop_5
    is_key: false
    name: prop5
    part_of_key: false
    type: INTEGER
  - alias: null
    column_mapping: prop_6
    is_key: false
    name: prop6
    part_of_key: false
    type: FLOAT
  source_name: file.csv
relationships:
- properties:
  - alias: null
    column_mapping: prop_7
    is_key: false
    name: prop7
    part_of_key: false
    type: FLOAT
  source: NodeA
  source_name: file.csv
  target: NodeB
  type: RELATIONSHIP_AB
"""
