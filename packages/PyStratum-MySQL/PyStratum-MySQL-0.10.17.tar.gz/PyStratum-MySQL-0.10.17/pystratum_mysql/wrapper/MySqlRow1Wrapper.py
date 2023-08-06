"""
PyStratum
"""
from typing import Dict, Any

from pystratum.wrapper.Row1Wrapper import Row1Wrapper
from pystratum_mysql.wrapper.MySqlWrapper import MySqlWrapper


class MySqlRow1Wrapper(MySqlWrapper, Row1Wrapper):
    """
    Wrapper method generator for stored procedures that are selecting 1 row.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def _write_result_handler(self, routine: Dict[str, Any]) -> None:
        self._write_line('return StaticDataLayer.execute_sp_row1({0!s})'.format(self._generate_command(routine)))

# ----------------------------------------------------------------------------------------------------------------------
