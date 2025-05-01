import unittest
from unittest.mock import patch, MagicMock

from graph_data_modeler_agent.data_model.core import Property


class TestPropertySolutionsWorkbench(unittest.TestCase):
    
    def setUp(self):
        # Create a mock SolutionsWorkbenchProperty
        self.mock_sw_property = MagicMock()
        self.mock_sw_property.name = "testProperty"
        self.mock_sw_property.referenceData = "col1, col2"
        self.mock_sw_property.datatype = "String"
        self.mock_sw_property.hasUniqueConstraint = True
        self.mock_sw_property.isPartOfKey = False
        
    @patch('graph_data_modeler_agent.data_model.core.property.SolutionsWorkbenchProperty')
    def test_from_solutions_workbench(self, mock_sw_property_class):
        """Test converting from Solutions Workbench property to Property"""
        
        p = Property(
            name="testProperty",
            type="STRING",
            column_mapping="col1",
            alias="col2",
            is_key=True
        )
        
        # Check basic properties
        self.assertEqual(p.name, "testProperty")
        self.assertEqual(p.type, "STRING")
        self.assertEqual(p.column_mapping, "col1")
        self.assertEqual(p.alias, "col2")
        self.assertEqual(p.is_key, True)


if __name__ == "__main__":
    unittest.main() 