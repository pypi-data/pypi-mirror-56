"""
PyStratum
"""
from typing import Dict, Any

from pystratum.style.PyStratumStyle import PyStratumStyle

from pystratum.RoutineWrapperGenerator import RoutineWrapperGenerator

from pystratum_mysql.MySqlConnection import MySqlConnection
from pystratum_mysql.wrapper import create_routine_wrapper


class MySqlRoutineWrapperGenerator(MySqlConnection, RoutineWrapperGenerator):
    """
    Class for generating a class with wrapper methods for calling stored routines in a MySQL database.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, io: PyStratumStyle):
        """
        Object constructor.

        :param PyStratumStyle io: The output decorator.
        """
        MySqlConnection.__init__(self, io)
        RoutineWrapperGenerator.__init__(self, io)

    # ------------------------------------------------------------------------------------------------------------------
    def _read_configuration_file(self, config_filename: str) -> None:
        """
        Reads parameters from the configuration file.

        :param str config_filename: The name of the configuration file.
        """
        MySqlConnection._read_configuration_file(self, config_filename)
        RoutineWrapperGenerator._read_configuration_file(self, config_filename)

    # ------------------------------------------------------------------------------------------------------------------
    def _write_routine_function(self, routine: Dict[str, Any]) -> None:
        """
        Generates a complete wrapper method for a stored routine.

        :param dict routine: The metadata of the stored routine.
        """
        wrapper = create_routine_wrapper(routine, self._lob_as_string_flag)
        self._code += wrapper.write_routine_method(routine)

# ----------------------------------------------------------------------------------------------------------------------
