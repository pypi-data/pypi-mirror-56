"""
PyStratum
"""
from typing import Dict, Any

from pystratum_mysql.wrapper.MySqlWrapper import MySqlWrapper
from pystratum.wrapper.RowsWithIndexWrapper import RowsWithIndexWrapper


class MySqlRowsWithIndexWrapper(RowsWithIndexWrapper, MySqlWrapper):
    """
    Wrapper method generator for stored procedures whose result set must be returned using tree structure using a
    combination of non-unique columns.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def _write_execute_rows(self, routine: Dict[str, Any]) -> None:
        self._write_line('rows = StaticDataLayer.execute_sp_rows({0!s})'.format(self._generate_command(routine)))

# ----------------------------------------------------------------------------------------------------------------------
