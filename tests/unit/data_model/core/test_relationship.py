import unittest
from unittest.mock import patch

from graph_data_modeler_agent.data_model.core import Property, Relationship
from graph_data_modeler_agent.data_model.arrows import ArrowsRelationship


class TestRelationship(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.prop1 = Property(
            name="score",
            type="FLOAT",
            column_mapping="similarity_score",
            is_key=False,
        )
        cls.prop2 = Property(
            name="current", type="BOOLEAN", column_mapping="current", is_key=True
        )
        cls.source = "NodeA"
        cls.target = "NodeB"

    def test_init(self) -> None:
        relationship = Relationship(
            type="HAS_SIMILAR",
            properties=[self.prop1, self.prop2],
            source=self.source,
            target=self.target,
        )

        self.assertEqual(relationship.type, "HAS_SIMILAR")
        self.assertEqual(len(relationship.properties), 2)

    def test_properties(self) -> None:
        relationship = Relationship(
            type="HAS_SIMILAR",
            properties=[self.prop1, self.prop2],
            source=self.source,
            target=self.target,
        )

        self.assertEqual(relationship.property_names, ["score", "current"])

    def test_unique_properties(self) -> None:
        relationship = Relationship(
            type="HAS_SIMILAR",
            properties=[self.prop1, self.prop2],
            source=self.source,
            target=self.target,
        )

        self.assertEqual(relationship.unique_properties, [self.prop2])

    def test_property_column_mapping(self) -> None:
        relationship = Relationship(
            type="HAS_SIMILAR",
            properties=[self.prop1, self.prop2],
            source=self.source,
            target=self.target,
        )

        self.assertEqual(
            relationship.property_column_mapping,
            {"score": "similarity_score", "current": "current"},
        )

    def test_unique_properties_column_mapping(self) -> None:
        relationship = Relationship(
            type="HAS_SIMILAR",
            properties=[self.prop1, self.prop2],
            source=self.source,
            target=self.target,
        )

        self.assertEqual(
            relationship.unique_properties_column_mapping, {"current": "current"}
        )

    @patch('graph_data_modeler_agent.data_model.core.relationship.Relationship.from_arrows')
    def test_from_arrows(self, mock_from_arrows) -> None:
        """
        Test init from arrows node.
        """
        # Create a mock return value for from_arrows
        mock_relationship = Relationship(
            type="HAS_SIMILAR",
            properties=[
                Property(name="score", type="FLOAT", column_mapping="similarity_score", is_key=False),
                Property(name="current", type="BOOLEAN", column_mapping="current", is_key=True)
            ],
            source="NodeA",
            target="NodeB",
        )
        mock_from_arrows.return_value = mock_relationship
        
        node_id_to_label_map = {"n0": "NodeA", "n1": "NodeB"}
        arrows_relationship = ArrowsRelationship(
            id="HAS_SIMILARNodeANodeB",
            type="HAS_SIMILAR",
            fromId="n0",
            toId="n1",
            properties={
                "score": "similarity_score | FLOAT",
                "current": "current | BOOLEAN",
                "csv": "test.csv",
            },
        )

        relationship_from_arrows = Relationship.from_arrows(
            arrows_relationship=arrows_relationship,
            node_id_to_label_map=node_id_to_label_map,
        )

        self.assertEqual(relationship_from_arrows.type, arrows_relationship.type)
        self.assertEqual(len(relationship_from_arrows.properties), 2)
        self.assertEqual(relationship_from_arrows.source.lower(), "nodea".lower())
        self.assertEqual(relationship_from_arrows.target.lower(), "nodeb".lower())
        self.assertFalse(relationship_from_arrows.properties[0].is_key)
        self.assertEqual(relationship_from_arrows.properties[0].type, "FLOAT")
        self.assertEqual(relationship_from_arrows.properties[1].type, "BOOLEAN")
        
        # Verify the mock was called with the expected arguments
        mock_from_arrows.assert_called_once_with(
            arrows_relationship=arrows_relationship,
            node_id_to_label_map=node_id_to_label_map,
        )


if __name__ == "__main__":
    unittest.main()
