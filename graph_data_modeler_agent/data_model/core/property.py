from typing import Dict, Optional

from pydantic import BaseModel, Field, ValidationInfo, field_validator
from pydantic.alias_generators import to_camel

from ...resources import (
    TYPES_MAP_NEO4J_TO_PYTHON,
    TYPES_MAP_PYTHON_TO_NEO4J,
    TYPES_MAP_PYTHON_TO_SOLUTIONS_WORKBENCH,
    TYPES_MAP_SOLUTIONS_WORKBENCH_TO_PYTHON,
    PythonTypeEnum,
)
from ..solutions_workbench import SolutionsWorkbenchProperty

NEO4J_TYPES = {
    "LIST",
    "MAP",
    "BOOLEAN",
    "INTEGER",
    "FLOAT",
    "STRING",
    "ByteArray",
    "DATE",
    "ZONED TIME",
    "LOCAL TIME",
    "ZONED DATETIME",
    "LOCAL DATETIME",
    "DURATION",
    "POINT",
}


class Property(BaseModel):
    """
    Property representation.

    Attributes
    ----------
    name : str
        The property name in Neo4j.
    type : str
        The Neo4j type of the property.
    column_mapping : str
        Which column the property is found under.
    alias : Optional[str]
        An optional second column that also indicates this property.
    is_key : bool
        Whether the property is a unique identifier.
    """

    name: str = Field(..., description="The property name in Neo4j.")
    type: str = Field(..., description="The Neo4j type of the property.")
    column_mapping: str = Field(
        ..., description="The source column that maps to the property."
    )
    alias: Optional[str] = Field(
        None,
        description="A foreign key column from another source file that maps to the property.",
    )
    is_key: bool = Field(
        False, description="Whether the property is a unique identifier."
    )

    @field_validator("name")
    def validate_name(cls, name: str, info: ValidationInfo) -> str:
        apply_neo4j_naming_conventions: bool = (
            info.context.get("apply_neo4j_naming_conventions", True)
            if info.context is not None
            else True
        )

        if apply_neo4j_naming_conventions:
            return to_camel(name)

        return name

    @field_validator("type", mode="before")
    def validate_type(cls, v: str) -> str:
        if v.upper() in NEO4J_TYPES:
            return v.upper()
        elif v.lower() == "object" or v.lower() == "string":
            return "STRING"
        elif "float" in v.lower():
            return "FLOAT"
        elif v.lower().startswith("int"):
            return "INTEGER"
        elif "bool" in v.lower():
            return "BOOLEAN"
        elif v.lower().startswith("list"):
            return "LIST"
        elif v.lower() == "date" or v.lower() == "datetime":
            return "DATE"
        else:
            raise ValueError(
                f"Invalid Property type given: {v}. Must be one of: {NEO4J_TYPES}"
            )

    def get_schema(self, verbose: bool = True, neo4j_typing: bool = False) -> str:
        """
        Get the Property schema.

        Parameters
        ----------
        verbose : bool, optional
            Whether to provide more detail, by default True
        neo4j_typing : bool, optional
            Whether to use Neo4j types instead of Python types, by default False

        Returns
        -------
        str
            The schema
        """

        ending = ""
        if self.is_key:
            ending = " | KEY"

        if verbose:
            return (
                f"{self.name} ({self.column_mapping}): {self.type}"
                + ending
            )
        else:
            return f"{self.name}: {self.type}"

    @property
    def neo4j_type(self) -> str:
        """
        The Neo4j property type.
        """
        return TYPES_MAP_PYTHON_TO_NEO4J[self.type]

    @classmethod
    def from_arrows(
        cls, arrows_property: Dict[str, str], caption: str = ""
    ) -> "Property":
        """
        Parse the arrows property representation into a standard Property model.
        Arrow property values are formatted as <column_mapping> | <python_type> | <unique, nodekey> | <ignore>.
        """

        column_mapping: str = ""
        if "|" in list(arrows_property.values())[0]:
            prop_props = [
                x.strip() for x in list(arrows_property.values())[0].split("|")
            ]
            if "," in prop_props[0]:
                column_mapping, alias = [x.strip() for x in prop_props[0].split(",")]
            else:
                column_mapping = prop_props[0]
                alias = None

            python_type = prop_props[1]
            # Convert to a Neo4j type if it's a Python type
            if python_type in TYPES_MAP_PYTHON_TO_NEO4J:
                neo4j_type = TYPES_MAP_PYTHON_TO_NEO4J[python_type]
            else:
                # Handle common Python types not in the mapping
                if python_type.lower() == "str" or python_type.lower() == "string":
                    neo4j_type = "STRING"
                elif python_type.lower() == "int" or python_type.lower() == "integer":
                    neo4j_type = "INTEGER"
                elif python_type.lower() == "float":
                    neo4j_type = "FLOAT"
                elif python_type.lower() == "bool" or python_type.lower() == "boolean":
                    neo4j_type = "BOOLEAN"
                elif python_type.lower().startswith("list"):
                    neo4j_type = "LIST"
                elif python_type.lower() == "dict" or python_type.lower() == "map":
                    neo4j_type = "MAP"
                elif python_type.lower() == "date" or python_type.lower() == "datetime":
                    neo4j_type = "DATE"
                else:
                    neo4j_type = "STRING"  # Default to string
            
            is_key = "unique" in prop_props or "nodekey" in prop_props
        else:
            column_mapping = list(arrows_property.values())[0]
            neo4j_type = "STRING"  # Default to string for unknown types
            alias = None
            is_key = False

        return cls(
            name=list(arrows_property.keys())[0],
            column_mapping=column_mapping,
            alias=alias,
            type=neo4j_type,
            is_key=is_key,
        )

    @classmethod
    def from_solutions_workbench(
        cls, solutions_workbench_property: SolutionsWorkbenchProperty
    ) -> "Property":
        """
        Parse the Solutions Workbench property into the standard property representation.
        """

        if "," in solutions_workbench_property.referenceData:
            column_mapping, alias = [
                x.strip() for x in solutions_workbench_property.referenceData.split(",")
            ]
        else:
            column_mapping, alias = (
                solutions_workbench_property.referenceData,
                None,
            )

        return cls(
            name=solutions_workbench_property.name,
            column_mapping=column_mapping,
            alias=alias,
            type=TYPES_MAP_SOLUTIONS_WORKBENCH_TO_PYTHON[
                solutions_workbench_property.datatype
            ],
            is_key=solutions_workbench_property.hasUniqueConstraint or solutions_workbench_property.isPartOfKey,
        )

    def to_solutions_workbench(self) -> "SolutionsWorkbenchProperty":
        """
        Parse into a Solutions Workbench property representation.
        """
        if self.alias:
            reference_data = f"{self.column_mapping}, {self.alias}"
        else:
            reference_data = self.column_mapping

        return SolutionsWorkbenchProperty(
            key=self.name,
            name=self.name,
            datatype=TYPES_MAP_PYTHON_TO_SOLUTIONS_WORKBENCH[self.type],
            referenceData=reference_data,
            isPartOfKey=self.is_key,
            isIndexed=self.is_key,
            mustExist=self.is_key,
            hasUniqueConstraint=self.is_key,
            isArray=True if self.type.startswith("List") else False,
        )
