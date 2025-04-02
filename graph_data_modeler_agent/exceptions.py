"""
This file contains all custom exceptions found in Runway.
"""


class GDMAError(Exception):
    """
    Global error for graph data modeler agent.
    """


class GDMAPydanticValidationError(ValueError):
    """Global error for handling Pydantic errors in GDMA"""


class Neo4jVersionError(GDMAError):
    """Exception raised when Neo4j version does not meet minimum requirements."""

    pass


class APOCVersionError(GDMAError):
    """Exception raised when APOC version does not meet minimum requirements."""

    pass


class APOCNotInstalledError(GDMAError):
    """Exception raised when APOC is required for operation, but not installed on Neo4j instance."""

    pass


class InvalidDataModelGenerationError(GDMAError):
    """Exception raised when an invalid data model is returned by an LLM after all retry attempts have been exhausted."""

    pass


class InvalidArrowsDataModelError(GDMAError):
    """Exception raised when an arrows.app data model is unable to be parsed into a Runway core data model."""

    pass


class InvalidSolutionsWorkbenchDataModelError(GDMAError):
    """Exception raised when a Solutions Workbench data model is unable to be parsed into a Runway core data model."""

    pass


class DataNotSupportedError(GDMAError):
    """Exception raised when an unsupported data format is given to a DataLoader class."""

    pass


class LoadCSVCypherGenerationError(GDMAError):
    """Exception raised when no standard clause can be constructed from provided arguments."""

    pass


class PandasDataSummariesNotGeneratedError(GDMAError):
    """Exception raised when the Discovery class 'run' method is ran and Pandas data summaries are not generated."""

    pass


class InvalidSourceNameError(GDMAPydanticValidationError):
    """Exception raised when an invalid `source_name` is provided."""

    pass


class NonuniqueNodeError(GDMAPydanticValidationError):
    """Exception raised when a node has no unique properties."""

    pass
