from typing import Any, Dict, List

from pydantic import BaseModel

from .column import Column
from .table_schema import TableSchema


class DataDictionary(BaseModel):
    table_schemas: List[TableSchema]

    @property
    def is_multifile(self) -> bool:
        """
        Whether the data dictionary contains more than 1 file.

        Returns
        -------
        bool
        """

        return len(self.table_schemas) > 1

    @property
    def table_column_names_dict(self) -> Dict[str, List[str]]:
        """
        A dictionary with table name keys and column list values.

        Returns
        -------
        Dict[str, List[str]]
            The dictionary.
        """

        return {ts.name: ts.column_names for ts in self.table_schemas}

    @property
    def table_columns_dict(self) -> Dict[str, List[Column]]:
        """
        A dictionary with table name keys and `Column` list values.

        Returns
        -------
        Dict[str, List[Column]]
            The dictionary.
        """

        return {ts.name: ts.columns for ts in self.table_schemas}

    @property
    def compact_dict(self) -> Dict[str, Any]:
        """
        Compact representation of the `DataDictionary` information.
        Format:
            {
            file_name:
                {
                    column_name: <description> Has aliases <aliases> | <ignore>,
                    ...
                },
            ...
            }

        Returns
        -------
        Dict[str, Any]
            A dictionary.
        """
        compact_info: Dict[str, str] = dict()
        [compact_info.update(ts.compact_dict) for ts in self.table_schemas]
        return compact_info
