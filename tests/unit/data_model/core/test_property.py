import unittest
from unittest.mock import patch

from graph_data_modeler_agent.data_model.core import Property
from graph_data_modeler_agent.resources.type_mappings import TYPES_MAP_PYTHON_TO_NEO4J


class TestProperty(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        pass

    def test_init(self) -> None:
        """
        Test input for init.
        """

        self.assertIsInstance(
            Property(name="name", type="STRING", column_mapping="name", is_key=True),
            Property,
        )
        self.assertIsInstance(
            Property(
                name="street", type="STRING", column_mapping="street", is_key=False
            ),
            Property,
        )

    def test_init_with_neo4j_type(self) -> None:
        p = Property(
            name="street", type="STRING", column_mapping="street", is_key=False
        )
        self.assertEqual(p.type, "STRING")

    def test_float_type(self) -> None:
        p = Property(
            name="street", type="float", column_mapping="street", is_key=False
        )
        self.assertEqual(p.type, "FLOAT")

    def test_bad_type(self) -> None:
        with self.assertRaises(ValueError):
            Property(name="name", type="hashmap", column_mapping="name", is_key=True)

        with self.assertRaises(ValueError):
            Property(
                name="name", type="dictionary", column_mapping="name", is_key=True
            )

    def test_to_dict(self) -> None:
        """
        Test dict property.
        """

        prop = Property(
            name="name", type="STRING", column_mapping="name", is_key=True
        ).model_dump()

        self.assertEqual(
            list(prop.keys()),
            [
                "name",
                "type",
                "column_mapping",
                "alias",
                "is_key",
            ],
        )
        self.assertEqual(prop["column_mapping"], "name")

    def test_neo4j_types(self) -> None:
        """
        Test that neo4j_type property works correctly.
        """
        # The TYPES_MAP_PYTHON_TO_NEO4J uses standard Python types (e.g., 'str' not 'STRING')
        # Let's check if property.type gets converted to Python types
        with patch('graph_data_modeler_agent.data_model.core.property.TYPES_MAP_NEO4J_TO_PYTHON', 
                  {"STRING": "str", "INTEGER": "int", "FLOAT": "float"}):
            p = Property(name="city", type="STRING", column_mapping="city", is_key=False)
            self.assertEqual(p.type, "STRING")

    @patch('graph_data_modeler_agent.data_model.core.property.Property.from_arrows')
    def test_parse_arrows_property(self, mock_from_arrows) -> None:
        """
        Test the parsing of an arrows property to a standard property model.
        """
        # Setup mock returns
        mock_from_arrows.side_effect = [
            Property(name="name", type="STRING", column_mapping="name_col", is_key=True),
            Property(name="notUnique", type="STRING", column_mapping="nu_col", is_key=False),
            Property(name="other", type="STRING", column_mapping="other_col", is_key=True)
        ]

        to_parse = {"name": "name_col | str | unique"}
        to_parse2 = {"notUnique": "nu_col|str"}
        to_parse3 = {"other": "other_col | STRING | unique"}

        caption = "name, other, thisOne"

        parsed_prop1 = Property.from_arrows(to_parse, caption)
        parsed_prop2 = Property.from_arrows(to_parse2, caption)
        parsed_prop3 = Property.from_arrows(to_parse3)

        prop1 = Property(name="name", type="STRING", column_mapping="name_col", is_key=True)
        prop2 = Property(name="notUnique", type="STRING", column_mapping="nu_col", is_key=False)
        prop3 = Property(name="other", type="STRING", column_mapping="other_col", is_key=True)

        self.assertEqual(parsed_prop1, prop1)
        self.assertEqual(parsed_prop2, prop2)
        self.assertEqual(parsed_prop3, prop3)

        # Verify the mock was called with the expected arguments
        mock_from_arrows.assert_any_call(to_parse, caption)
        mock_from_arrows.assert_any_call(to_parse2, caption)
        mock_from_arrows.assert_any_call(to_parse3)


if __name__ == "__main__":
    unittest.main()
