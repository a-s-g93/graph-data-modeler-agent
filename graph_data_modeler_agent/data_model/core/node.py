from typing import Dict, List, Tuple, Union

from pydantic import (
    BaseModel,
    Field,
    ValidationError,
    ValidationInfo,
    field_validator,
    model_validator,
)
from pydantic.alias_generators import to_pascal, to_snake
from pydantic_core import InitErrorDetails, PydanticCustomError

from ...exceptions import (
    InvalidSourceNameError,
    NonuniqueNodeError,
)
from ..arrows import ArrowsNode
from ..solutions_workbench import SolutionsWorkbenchNode
from .property import Property


class Node(BaseModel):
    """
    Standard Node representation.
    A node is an entity in the database.
    A node is defined by its label and properties.
    A node must have at least one key property that uniquely identifies it.

    Attributes
    -------
    label : str
        The node label.
    properties : List[Property]
        A list of the properties within the node.
    source_name : str, optional
        The name of the file containing the node's information.
    """

    label: str = Field(..., description="The node label.")
    properties: List[Property] = Field(
        ..., description="The properties within the node."
    )
    source_name: str = Field(
        ..., description="The name of the file containing the node's information."
    )

    def __str__(self) -> str:
        return f"(:{self.label})"

    def get_schema(self, verbose: bool = True, neo4j_typing: bool = False) -> str:
        """
        Get the Node schema.

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

        props = ""
        for p in self.properties:
            props += (
                "* " + p.get_schema(verbose=verbose, neo4j_typing=neo4j_typing) + "\n"
            )
        schema = f"""(:{self.label})
{props}"""

        return schema

    @property
    def property_names(self) -> List[str]:
        """
        The node property names.

        Returns
        -------
        List[str]
            A list of the property names in the node.
        """

        return [prop.name for prop in self.properties]

    @property
    def property_column_mapping(self) -> Dict[str, Union[str, List[str]]]:
        """
        A map of property names to their respective CSV columns.

        Returns
        -------
        Dict[str, str | List[str]]
            A dictionary with property name keys and CSV column values.
        """

        return {prop.name: prop.column_mapping for prop in self.properties}

    @property
    def unique_properties(self) -> List[Property]:
        """
        The node's unique properties.

        Returns
        -------
        List[Property]
            A list of unique properties.
        """

        return [prop for prop in self.properties if prop.is_key]

    @property
    def unique_properties_column_mapping(self) -> Dict[str, Union[str, List[str]]]:
        """
        Map of unique properties to their respective CSV columns.

        Returns
        -------
        Dict[str, str | List[str]]
            A dictionary with unique property name keys and CSV column values.
        """

        return {
            prop.name: prop.column_mapping for prop in self.properties if prop.is_key
        }

    @property
    def nonunique_properties(self) -> List[Property]:
        """
        The node's nonunique properties.

        Returns
        -------
        List[str]
            A list of nonunique properties.
        """

        return [prop for prop in self.properties if not prop.is_key]

    @property
    def nonunique_properties_column_mapping(self) -> Dict[str, str]:
        """
        Map of nonunique properties to their respective CSV columns.

        Returns
        -------
        Dict[str, str | List[str]]
            A dictionary with nonunique property name keys and CSV column values.
        """

        return {
            prop.name: prop.column_mapping
            for prop in self.properties
            if not prop.is_key
        }

    @property
    def node_keys(self) -> List[Property]:
        """
        The node key properties, if any.

        Returns
        -------
        List[Property]
            A list of the properties that make up a node key, if any.
        """

        return [prop for prop in self.properties if prop.is_key]

    @property
    def node_key_mapping(self) -> Dict[str, str]:
        """
        Map of node keys to their respective csv columns.

        Returns
        -------
        Dict[str, str]
            A dictionary with node key property keys and CSV column values.
        """

        return {
            prop.name: prop.column_mapping for prop in self.properties if prop.is_key
        }

    @property
    def nonunique_properties_mapping_for_set_clause(self) -> Dict[str, str]:
        """
        Map of nonunique properties to their respective csv columns if a property is not unique or a node key.

        Returns
        -------
        Dict[str, str]
            A dictionary of nonunique or non node key property keys and CSV column values.
        """

        return {
            prop.name: prop.column_mapping
            for prop in self.properties
            if not prop.is_key
        }

    @property
    def nonidentifying_properties(self) -> List[Property]:
        """
        List of nonidentifying properties.

        Returns
        -------
        List[Property]
            A list with unique or node key property keys and CSV column values.
        """

        return [prop for prop in self.properties if not prop.is_key]

    @property
    def node_key_aliases(self) -> List[Property]:
        """
        List of node key properties with aliases, if they exist.

        Returns
        -------
        List[Property]
            The aliases.
        """

        return [p for p in self.properties if p.is_key and p.alias is not None]

    @property
    def unique_property_aliases(self) -> List[Property]:
        """
        List of unique properties with aliases, if they exist.

        Returns
        -------
        List[Property]
            The aliases.
        """

        return [p for p in self.properties if p.is_key and p.alias is not None]

    @field_validator("label")
    def validate_source_naming(cls, label: str, info: ValidationInfo) -> str:
        apply_neo4j_naming_conventions: bool = (
            info.context.get("apply_neo4j_naming_conventions", True)
            if info.context is not None
            else True
        )

        if apply_neo4j_naming_conventions and not label[0].isupper():
            return to_pascal(to_snake(label.lower()))

        return label

    @field_validator("source_name")
    def validate_source_name(cls, source_name: str, info: ValidationInfo) -> str:
        valid_sources: List[str] = (
            info.context.get("valid_sources", list())
            if info.context is not None
            else list()
        )

        # skip for single file input
        if len(valid_sources) == 1:
            return valid_sources[0]
        elif source_name in valid_sources or not valid_sources:
            return source_name
        else:
            raise InvalidSourceNameError(
                f"{source_name} is not in the provided file list: {valid_sources}."
            )

    @field_validator("properties")
    def enforce_uniqueness(
        cls, properties: List[Property], info: ValidationInfo
    ) -> List[Property]:
        enforce_uniqueness: bool = (
            info.context.get("enforce_uniqueness", True)
            if info.context is not None
            else True
        )
        if enforce_uniqueness:
            unique_properties = [prop for prop in properties if prop.is_key]

            if len(unique_properties) == 0:
                # keep it simple by asking only for a unique property, not to create a node key combo
                raise NonuniqueNodeError(
                    f"`Node` {info.data.get('label')} must contain a key `Property` in `properties` field."
                )

        return properties

    @model_validator(mode="after")
    def validate_property_mappings(self, info: ValidationInfo) -> "Node":
        # Use table_column_listings if provided in context
        table_column_listings: Dict[str, List[str]] = (
            info.context.get("table_column_listings", {})
            if info.context is not None
            else {}
        )
        
        # If table_column_listings is not provided but valid_columns is, use valid_columns
        valid_columns: Dict[str, List[str]] = (
            info.context.get("valid_columns", {})
            if info.context is not None
            else {}
        )
        
        if not table_column_listings and valid_columns:
            table_column_listings = valid_columns
        
        errors: List[InitErrorDetails] = list()

        if table_column_listings:
            for prop in self.properties:
                if prop.column_mapping not in table_column_listings.get(
                    self.source_name, list()
                ):
                    errors.append(
                        InitErrorDetails(
                            type=PydanticCustomError(
                                "invalid_column_mapping_error",
                                f"The `Node` {self.label} has the `Property` {prop.name} mapped to column {prop.column_mapping} which is not allowed for source file {self.source_name}. Removed {prop.name} from `Node` {self.label}.",
                            ),
                            loc=("properties",),
                            input=self.properties,
                            ctx={},
                        )
                    )

        if errors:
            raise ValidationError.from_exception_data(
                title=self.__class__.__name__,
                line_errors=errors,
            )

        return self

    def to_arrows(self, x_position: float, y_position: float) -> ArrowsNode:
        """
        Return an arrows.app compatible node.
        """
        pos = {"x": x_position, "y": y_position}
        props = {
            x.name: x.column_mapping
            + " | "
            + x.type
            + (" | nodekey" if x.is_key else "")
            for x in self.properties
        }

        return ArrowsNode(
            id=self.label,
            caption=self.source_name,
            position=pos,
            labels=[self.label],
            properties=props,
        )

    @classmethod
    def from_arrows(cls, arrows_node: ArrowsNode) -> "Node":
        """
        Initialize a Node from an arrows node.
        """

        props = [
            Property.from_arrows(arrows_property={k: v})
            for k, v in arrows_node.properties.items()
            if k != "csv" and not v.lower().rstrip().endswith("ignore")
        ]

        source_name = (
            arrows_node.properties["csv"]
            if "csv" in arrows_node.properties.keys()
            else arrows_node.caption
        )

        # support only single labels for now, take first label
        return cls(
            label=arrows_node.labels[0], properties=props, source_name=source_name
        )

    def to_solutions_workbench(
        self, key: str, x: int, y: int
    ) -> "SolutionsWorkbenchNode":
        """
        Return a Solutions Workbench compatible Node.
        """

        props = {prop.name: prop.to_solutions_workbench() for prop in self.properties}

        return SolutionsWorkbenchNode(
            key=key,
            label=self.label,
            properties=props,
            x=x,
            y=y,
            description=self.source_name,
        )

    @classmethod
    def from_solutions_workbench(
        cls, solutions_workbench_node: SolutionsWorkbenchNode
    ) -> "Node":
        """
        Initialize a core Node from a Solutions Workbench Node.
        """

        props = [
            Property.from_solutions_workbench(solutions_workbench_property=prop)
            for prop in solutions_workbench_node.properties.values()
        ]

        source_name = solutions_workbench_node.description

        # support only single labels for now, take first label
        return cls(
            label=solutions_workbench_node.label,
            properties=props,
            source_name=source_name,
        )


class Nodes(BaseModel):
    nodes: List[Node] = Field(
        description="A list of nodes to be used in a graph data model."
    )

    @field_validator("nodes")
    def validate_nodes(cls, nodes: List[Node]) -> List[Node]:
        assert len(nodes) > 1, "`nodes` must contain more than 1 `Node`."

        return nodes

    @model_validator(mode="after")
    def advanced_validation(self, info: ValidationInfo) -> "Nodes":
        errors: List[InitErrorDetails] = list()

        def _parse_duplicated_property_location(
            context: Tuple[str, str, int, str, int, str],
        ) -> Tuple[str, int, str, int, str]:
            """Parse the location of a duplicated property in the data model and return the location formatted for Pydantic Error reporting."""
            #         n or r     n or r idx   properties   prop idx
            return (context[1], context[2], context[3], context[4], "column_mapping")

        def _validate_column_mappings_used_only_once() -> List[InitErrorDetails]:
            """
            Validate that each column mapping is used no more than one time in the data model.
            This check may be skipped by providing `allow_duplicate_column_mappings` = True in the validation context.
            """

            allow_duplicate_column_mappings: bool = (
                info.context.get("allow_duplicate_column_mappings", False)
                if info.context is not None
                else False
            )
            errors: List[InitErrorDetails] = list()

            if not allow_duplicate_column_mappings:
                used_features: Dict[
                    str, Dict[str, List[Tuple[str, str, int, str, int, str]]]
                ] = dict()
                # --- used_features example ---
                # file to column to labels or types
                # {
                # "a.csv": {"feature_a": ["LabelA", "LabelB"]},
                # "b.csv": {"feature_b": ["LabelA", "LabelB"],
                #           "feature_c": ["LabelD"]},
                # "c.csv": {}
                # }
                # -----------------------------

                for node_idx, node in enumerate(self.nodes):
                    # init the file dictionary
                    if node.source_name not in used_features.keys():
                        used_features[node.source_name] = dict()
                    for prop_idx, prop in enumerate(node.properties):
                        if prop.column_mapping not in list(
                            used_features[node.source_name].keys()
                        ):
                            used_features[node.source_name][prop.column_mapping] = [
                                (
                                    node.label,
                                    "nodes",
                                    node_idx,
                                    "properties",
                                    prop_idx,
                                    "column_mapping",
                                )
                            ]
                        else:
                            used_features[node.source_name][prop.column_mapping].append(
                                (
                                    node.label,
                                    "nodes",
                                    node_idx,
                                    "properties",
                                    prop_idx,
                                    "column_mapping",
                                )
                            )

                for source_name, feature_dict in used_features.items():
                    for prop_mapping, labels_or_types in feature_dict.items():
                        if len(labels_or_types) > 1:
                            for l_or_t in labels_or_types:
                                errors.append(
                                    InitErrorDetails(
                                        type=PydanticCustomError(
                                            "duplicate_property_column_mapping_error",
                                            f"{source_name} column '{prop_mapping}' may only be used once as a `Property`.`column_mapping` value. Consider removing this property from `Node` '{l_or_t[0]}'.",
                                        ),
                                        loc=_parse_duplicated_property_location(
                                            context=l_or_t
                                        ),
                                        input=prop_mapping,
                                        ctx={},
                                    )
                                )

            return errors

        errors.extend(_validate_column_mappings_used_only_once())

        if errors:
            raise ValidationError.from_exception_data(
                title=self.__class__.__name__,
                line_errors=errors,
            )

        return self
