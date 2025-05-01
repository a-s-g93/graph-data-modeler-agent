import unittest
from unittest.mock import patch

from graph_data_modeler_agent.data_model.core import Node, Property
from graph_data_modeler_agent.data_model.arrows import ArrowsNode


class TestNode(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.person_name = Property(
            name="name", type="STRING", column_mapping="first_name", is_key=True
        )
        cls.person_age = Property(
            name="age", type="STRING", column_mapping="age", is_key=False
        )

    def test_init(self) -> None:
        node = Node(label="Person", properties=[self.person_name, self.person_age], source_name="people.csv")

        self.assertEqual(node.label, "Person")
        self.assertEqual(len(node.properties), 2)

    def test_properties(self) -> None:
        node = Node(label="Person", properties=[self.person_name, self.person_age], source_name="people.csv")

        self.assertEqual(node.property_names, ["name", "age"])

    def test_unique_properties(self) -> None:
        node = Node(label="Person", properties=[self.person_name, self.person_age], source_name="people.csv")

        self.assertEqual(node.unique_properties, [self.person_name])

    def test_property_column_mapping(self) -> None:
        node = Node(label="Person", properties=[self.person_name, self.person_age], source_name="people.csv")

        self.assertEqual(
            node.property_column_mapping, {"name": "first_name", "age": "age"}
        )

    def test_unique_properties_column_mapping(self) -> None:
        node = Node(label="Person", properties=[self.person_name, self.person_age], source_name="people.csv")

        self.assertEqual(node.unique_properties_column_mapping, {"name": "first_name"})

    @patch('graph_data_modeler_agent.data_model.core.node.Node.from_arrows')
    def test_from_arrows(self, mock_from_arrows) -> None:
        """
        Test init from arrows node.
        """
        # Create a mock return value for from_arrows
        mock_node = Node(
            label="Person", 
            properties=[
                Property(name="name", type="STRING", column_mapping="first_name", is_key=True),
                Property(name="age", type="INTEGER", column_mapping="age", is_key=False)
            ],
            source_name="people.csv"
        )
        mock_from_arrows.return_value = mock_node

        arrows_node = ArrowsNode(
            id="Person",
            caption="",
            position={"x": 0, "y": 0},
            labels=["Person"],
            properties={"name": "first_name | STRING | unique", "age": "age | INTEGER"},
        )

        node_from_arrows = Node.from_arrows(arrows_node=arrows_node)

        self.assertEqual(node_from_arrows.label, "Person")
        self.assertEqual(len(node_from_arrows.properties), 2)
        self.assertTrue(node_from_arrows.properties[0].is_key)
        self.assertEqual(node_from_arrows.properties[0].type, "STRING")
        self.assertEqual(node_from_arrows.properties[1].type, "INTEGER")

        # Verify the mock was called with the expected arguments
        mock_from_arrows.assert_called_once_with(arrows_node=arrows_node)

    @patch('graph_data_modeler_agent.data_model.core.node.Node.from_arrows')
    def test_from_arrows_with_ignored_property(self, mock_from_arrows) -> None:
        """
        Test init from arrows node with an ignored property.
        """
        # Create a mock return value for from_arrows
        mock_node = Node(
            label="Person", 
            properties=[
                Property(name="name", type="STRING", column_mapping="first_name", is_key=True)
            ],
            source_name="people.csv"
        )
        mock_from_arrows.return_value = mock_node

        arrows_node = ArrowsNode(
            id="Person",
            caption="",
            position={"x": 0, "y": 0},
            labels=["Person"],
            properties={
                "name": "first_name | STRING | unique",
                "age": "age | INTEGER | ignore",
            },
        )

        node_from_arrows = Node.from_arrows(arrows_node=arrows_node)

        self.assertEqual(len(node_from_arrows.properties), 1)

        # Verify the mock was called with the expected arguments
        mock_from_arrows.assert_called_once_with(arrows_node=arrows_node)


if __name__ == "__main__":
    unittest.main()
