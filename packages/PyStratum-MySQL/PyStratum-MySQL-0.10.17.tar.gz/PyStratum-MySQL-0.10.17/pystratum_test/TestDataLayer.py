from typing import Any, Dict, List, Optional

from pystratum_mysql.StaticDataLayer import StaticDataLayer


# ----------------------------------------------------------------------------------------------------------------------
class TestDataLayer(StaticDataLayer):
    """
    The stored routines wrappers.
    """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_constant01() -> Any:
        """
        Test for constant.

        :rtype: dict[str,*]
        """
        return StaticDataLayer.execute_sp_row1("call tst_constant01()")

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_magic_constant01() -> Any:
        """
        Test for magic constant.

        :rtype: *
        """
        return StaticDataLayer.execute_sp_singleton1("call tst_magic_constant01()")

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_magic_constant02() -> Any:
        """
        Test for magic constant.

        :rtype: *
        """
        return StaticDataLayer.execute_sp_singleton1("call tst_magic_constant02()")

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_magic_constant03() -> Any:
        """
        Test for magic constant.

        :rtype: *
        """
        return StaticDataLayer.execute_sp_singleton1("call tst_magic_constant03()")

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_magic_constant04() -> Any:
        """
        Test for magic constant.

        :rtype: *
        """
        return StaticDataLayer.execute_sp_singleton1("call tst_magic_constant04()")

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_parameter_types01(p_param00: Optional[int], p_param01: Optional[int], p_param02: Optional[int], p_param03: Optional[int], p_param04: Optional[int], p_param05: Optional[float], p_param06: Optional[float], p_param07: Optional[float], p_param08: Optional[int], p_param09: Optional[str], p_param10: Optional[str], p_param11: Optional[str], p_param12: Optional[str], p_param13: Optional[int], p_param14: Optional[str], p_param15: Optional[str], p_param16: Optional[bytes], p_param17: Optional[bytes], p_param26: Optional[str], p_param27: Optional[str]) -> int:
        """
        Test for all possible types of parameters excluding LOB's.

        :param int p_param00: Test parameter 00.
                              int(11)
        :param int p_param01: Test parameter 01.
                              smallint(6)
        :param int p_param02: Test parameter 02.
                              tinyint(4)
        :param int p_param03: Test parameter 03.
                              mediumint(9)
        :param int p_param04: Test parameter 04.
                              bigint(20)
        :param float p_param05: Test parameter 05.
                                decimal(10,2)
        :param float p_param06: Test parameter 06.
                                float
        :param float p_param07: Test parameter 07.
                                double
        :param int p_param08: Test parameter 08.
                              bit(8)
        :param str p_param09: Test parameter 09.
                              date
        :param str p_param10: Test parameter 10.
                              datetime
        :param str p_param11: Test parameter 11.
                              timestamp
        :param str p_param12: Test parameter 12.
                              time
        :param int p_param13: Test parameter 13.
                              year(4)
        :param str p_param14: Test parameter 14.
                              char(10) character set utf8 collation utf8_general_ci
        :param str p_param15: Test parameter 15.
                              varchar(10) character set utf8 collation utf8_general_ci
        :param bytes p_param16: Test parameter 16.
                                binary(10)
        :param bytes p_param17: Test parameter 17.
                                varbinary(10)
        :param str p_param26: Test parameter 26.
                              enum('a','b') character set utf8 collation utf8_general_ci
        :param str p_param27: Test parameter 27.
                              set('a','b') character set utf8 collation utf8_general_ci

        :rtype: int
        """
        return StaticDataLayer.execute_sp_none("call tst_parameter_types01(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", p_param00, p_param01, p_param02, p_param03, p_param04, p_param05, p_param06, p_param07, p_param08, p_param09, p_param10, p_param11, p_param12, p_param13, p_param14, p_param15, p_param16, p_param17, p_param26, p_param27)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_parameter_types02(p_param00: Optional[int], p_param01: Optional[int], p_param02: Optional[int], p_param03: Optional[int], p_param04: Optional[int], p_param05: Optional[float], p_param06: Optional[float], p_param07: Optional[float], p_param08: Optional[int], p_param09: Optional[str], p_param10: Optional[str], p_param11: Optional[str], p_param12: Optional[str], p_param13: Optional[int], p_param14: Optional[str], p_param15: Optional[str], p_param16: Optional[bytes], p_param17: Optional[bytes], p_param18: Optional[bytes], p_param19: Optional[bytes], p_param20: Optional[bytes], p_param21: Optional[bytes], p_param22: Optional[str], p_param23: Optional[str], p_param24: Optional[str], p_param25: Optional[str], p_param26: Optional[str], p_param27: Optional[str]) -> int:
        """
        Test for all possible types of parameters including LOB's.

        :param int p_param00: Test parameter 00.
                              int(11)
        :param int p_param01: Test parameter 01.
                              smallint(6)
        :param int p_param02: Test parameter 02.
                              tinyint(4)
        :param int p_param03: Test parameter 03.
                              mediumint(9)
        :param int p_param04: Test parameter 04.
                              bigint(20)
        :param float p_param05: Test parameter 05.
                                decimal(10,2)
        :param float p_param06: Test parameter 06.
                                float
        :param float p_param07: Test parameter 07.
                                double
        :param int p_param08: Test parameter 08.
                              bit(8)
        :param str p_param09: Test parameter 09.
                              date
        :param str p_param10: Test parameter 10.
                              datetime
        :param str p_param11: Test parameter 11.
                              timestamp
        :param str p_param12: Test parameter 12.
                              time
        :param int p_param13: Test parameter 13.
                              year(4)
        :param str p_param14: Test parameter 14.
                              char(10) character set utf8 collation utf8_general_ci
        :param str p_param15: Test parameter 15.
                              varchar(10) character set utf8 collation utf8_general_ci
        :param bytes p_param16: Test parameter 16.
                                binary(10)
        :param bytes p_param17: Test parameter 17.
                                varbinary(10)
        :param bytes p_param18: Test parameter 18.
                                tinyblob
        :param bytes p_param19: Test parameter 19.
                                blob
        :param bytes p_param20: Test parameter 20.
                                mediumblob
        :param bytes p_param21: Test parameter 21.
                                longblob
        :param str p_param22: Test parameter 22.
                              tinytext character set utf8 collation utf8_general_ci
        :param str p_param23: Test parameter 23.
                              text character set utf8 collation utf8_general_ci
        :param str p_param24: Test parameter 24.
                              mediumtext character set utf8 collation utf8_general_ci
        :param str p_param25: Test parameter 25.
                              longtext character set utf8 collation utf8_general_ci
        :param str p_param26: Test parameter 26.
                              enum('a','b') character set utf8 collation utf8_general_ci
        :param str p_param27: Test parameter 27.
                              set('a','b') character set utf8 collation utf8_general_ci

        :rtype: int
        """
        return StaticDataLayer.execute_sp_none("call tst_parameter_types02(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", p_param00, p_param01, p_param02, p_param03, p_param04, p_param05, p_param06, p_param07, p_param08, p_param09, p_param10, p_param11, p_param12, p_param13, p_param14, p_param15, p_param16, p_param17, p_param18, p_param19, p_param20, p_param21, p_param22, p_param23, p_param24, p_param25, p_param26, p_param27)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_parameter_types03(p_param14: Optional[str], p_param15: Optional[str], p_param16: Optional[bytes], p_param17: Optional[bytes]) -> int:
        """
        Test for all possible types of parameters with maximum length.

        :param str p_param14: Test parameter 14.
                              char(255) character set utf8 collation utf8_general_ci
        :param str p_param15: Test parameter 15.
                              varchar(4096) character set utf8 collation utf8_general_ci
        :param bytes p_param16: Test parameter 16.
                                binary(255)
        :param bytes p_param17: Test parameter 17.
                                varbinary(4096)

        :rtype: int
        """
        return StaticDataLayer.execute_sp_none("call tst_parameter_types03(%s, %s, %s, %s)", p_param14, p_param15, p_param16, p_param17)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_bulk(bulk_handler) -> int:
        """
        Test for designation type bulk.

        :param pystratum.BulkHandler.BulkHandler bulk_handler: The bulk handler for processing the selected rows.

        :rtype: int
        """
        return StaticDataLayer.execute_sp_bulk(bulk_handler, "call tst_test_bulk()")

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_find_designation_type01() -> Any:
        """
        Test for designation type.

        :rtype: dict[str,*]
        """
        return StaticDataLayer.execute_sp_row1("call tst_test_find_designation_type01()")

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_find_designation_type02() -> Any:
        """
        Test for designation type.

        :rtype: dict[str,*]
        """
        return StaticDataLayer.execute_sp_row1("call tst_test_find_designation_type02()")

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_find_designation_type03() -> Any:
        """
        Test for designation type.

        :rtype: dict[str,*]
        """
        return StaticDataLayer.execute_sp_row1("call tst_test_find_designation_type03()")

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_find_designation_type04() -> Any:
        """
        Test for designation type.

        :rtype: dict[str,*]
        """
        return StaticDataLayer.execute_sp_row1("call tst_test_find_designation_type04()")

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_find_designation_type05() -> Any:
        """
        Test for designation type.

        :rtype: dict[str,*]
        """
        return StaticDataLayer.execute_sp_row1("call tst_test_find_designation_type05()")

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_function(p_a: Optional[int], p_b: Optional[int]) -> Any:
        """
        Test for stored function wrapper.

        :param int p_a: Parameter A.
                        int(11)
        :param int p_b: Parameter B.
                        int(11)

        :rtype: *
        """
        return StaticDataLayer.execute_singleton1("select tst_test_function(%s, %s)", p_a, p_b)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_log() -> int:
        """
        Test for designation type log.

        :rtype: int
        """
        return StaticDataLayer.execute_sp_log("call tst_test_log()")

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_max_allowed_packet(p_tmp_blob: Optional[bytes]) -> Any:
        """
        Test for sending data larger than max_allowed_packet.

        :param bytes p_tmp_blob: The BLOB larger than max_allowed_packet.
                                 longblob

        :rtype: *
        """
        return StaticDataLayer.execute_sp_singleton1("call tst_test_max_allowed_packet(%s)", p_tmp_blob)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_multi() -> List[List[Dict[str, Any]]]:
        """
        Test for designation type multi.

        :rtype: list[list[dict[str,*]]]
        """
        return StaticDataLayer.execute_sp_multi("call tst_test_multi()")

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_none1(p_count: Optional[int]) -> int:
        """
        Test for designation type none.

        :param int p_count: The number of iterations.
                            bigint(20)

        :rtype: int
        """
        return StaticDataLayer.execute_sp_none("call tst_test_none1(%s)", p_count)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_none2() -> int:
        """
        Test for designation type none.

        :rtype: int
        """
        return StaticDataLayer.execute_sp_none("call tst_test_none2()")

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_none_with_lob(p_count: Optional[int], p_blob: Optional[bytes]) -> int:
        """
        Test for designation type none with BLOB.

        :param int p_count: The number of iterations.
                            bigint(20)
        :param bytes p_blob: The BLOB.
                             blob

        :rtype: int
        """
        return StaticDataLayer.execute_sp_none("call tst_test_none_with_lob(%s, %s)", p_count, p_blob)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_percent_symbol() -> List[Dict[str, Any]]:
        """
        Test for stored function with percent symbols.

        :rtype: list[dict[str,*]]
        """
        return StaticDataLayer.execute_sp_rows("call tst_test_percent_symbol()")

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_row0a(p_count: Optional[int]) -> Any:
        """
        Test for designation type row0.

        :param int p_count: The number of rows selected.
                            * 0 For a valid test.
                            * 1 For a valid test.
                            * 2 For a invalid test.
                            int(11)

        :rtype: None|dict[str,*]
        """
        return StaticDataLayer.execute_sp_row0("call tst_test_row0a(%s)", p_count)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_row0a_with_lob(p_count: Optional[int], p_blob: Optional[bytes]) -> Any:
        """
        Test for designation type row0 with BLOB.

        :param int p_count: The number of rows selected.
                            * 0 For a valid test.
                            * 1 For a valid test.
                            * 2 For a invalid test.
                            int(11)
        :param bytes p_blob: The BLOB.
                             blob

        :rtype: None|dict[str,*]
        """
        return StaticDataLayer.execute_sp_row0("call tst_test_row0a_with_lob(%s, %s)", p_count, p_blob)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_row1a(p_count: Optional[int]) -> Any:
        """
        Test for designation type row1.

        :param int p_count: The number of rows selected.
                            * 0 For a invalid test.
                            * 1 For a valid test.
                            * 2 For a invalid test.
                            int(11)

        :rtype: dict[str,*]
        """
        return StaticDataLayer.execute_sp_row1("call tst_test_row1a(%s)", p_count)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_row1a_with_lob(p_count: Optional[int], p_blob: Optional[bytes]) -> Any:
        """
        Test for designation type row1 with BLOB.

        :param int p_count: The number of rows selected.
                            * 0 For a invalid test.
                            * 1 For a valid test.
                            * 2 For a invalid test.
                            int(11)
        :param bytes p_blob: The BLOB.
                             blob

        :rtype: dict[str,*]
        """
        return StaticDataLayer.execute_sp_row1("call tst_test_row1a_with_lob(%s, %s)", p_count, p_blob)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_rows1(p_count: Optional[int]) -> List[Dict[str, Any]]:
        """
        Test for designation type row1.

        :param int p_count: The number of rows selected.
                            * 0 For a invalid test.
                            * 1 For a valid test.
                            * 2 For a invalid test.
                            int(11)

        :rtype: list[dict[str,*]]
        """
        return StaticDataLayer.execute_sp_rows("call tst_test_rows1(%s)", p_count)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_rows1_with_lob(p_count: Optional[int], p_blob: Optional[bytes]) -> List[Dict[str, Any]]:
        """
        Test for designation type rows.

        :param int p_count: The number of rows selected.
                            int(11)
        :param bytes p_blob: The BLOB.
                             blob

        :rtype: list[dict[str,*]]
        """
        return StaticDataLayer.execute_sp_rows("call tst_test_rows1_with_lob(%s, %s)", p_count, p_blob)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_rows_with_index1(p_count: Optional[int]) -> Dict:
        """
        Test for designation type rows_with_index.

        :param int p_count: The number of rows selected.
                            int(11)

        :rtype: dict
        """
        ret = {}
        rows = StaticDataLayer.execute_sp_rows("call tst_test_rows_with_index1(%s)", p_count)
        for row in rows:
            if row['tst_c01'] in ret:
                if row['tst_c02'] in ret[row['tst_c01']]:
                    ret[row['tst_c01']][row['tst_c02']].append(row)
                else:
                    ret[row['tst_c01']][row['tst_c02']] = [row]
            else:
                ret[row['tst_c01']] = {row['tst_c02']: [row]}

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_rows_with_index1_with_lob(p_count: Optional[int], p_blob: Optional[bytes]) -> Dict:
        """
        Test for designation type rows_with_index with BLOB..

        :param int p_count: The number of rows selected.
                            int(11)
        :param bytes p_blob: The BLOB.
                             blob

        :rtype: dict
        """
        ret = {}
        rows = StaticDataLayer.execute_sp_rows("call tst_test_rows_with_index1_with_lob(%s, %s)", p_count, p_blob)
        for row in rows:
            if row['tst_c01'] in ret:
                if row['tst_c02'] in ret[row['tst_c01']]:
                    ret[row['tst_c01']][row['tst_c02']].append(row)
                else:
                    ret[row['tst_c01']][row['tst_c02']] = [row]
            else:
                ret[row['tst_c01']] = {row['tst_c02']: [row]}

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_rows_with_key1(p_count: Optional[int]) -> Dict:
        """
        Test for designation type rows_with_key.

        :param int p_count: Number of rows selected.
                            int(11)

        :rtype: dict
        """
        ret = {}
        rows = StaticDataLayer.execute_sp_rows("call tst_test_rows_with_key1(%s)", p_count)
        for row in rows:
            if row['tst_c01'] in ret:
                if row['tst_c02'] in ret[row['tst_c01']]:
                    if row['tst_c03'] in ret[row['tst_c01']][row['tst_c02']]:
                        raise Exception('Duplicate key for %s.' % str((row['tst_c01'], row['tst_c02'], row['tst_c03'])))
                    else:
                        ret[row['tst_c01']][row['tst_c02']][row['tst_c03']] = row
                else:
                    ret[row['tst_c01']][row['tst_c02']] = {row['tst_c03']: row}
            else:
                ret[row['tst_c01']] = {row['tst_c02']: {row['tst_c03']: row}}

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_rows_with_key1_with_lob(p_count: Optional[int], p_blob: Optional[bytes]) -> Dict:
        """
        Test for designation type rows_with_key with BLOB.

        :param int p_count: The number of rows selected.
                            int(11)
        :param bytes p_blob: The BLOB.
                             blob

        :rtype: dict
        """
        ret = {}
        rows = StaticDataLayer.execute_sp_rows("call tst_test_rows_with_key1_with_lob(%s, %s)", p_count, p_blob)
        for row in rows:
            if row['tst_c01'] in ret:
                if row['tst_c02'] in ret[row['tst_c01']]:
                    if row['tst_c03'] in ret[row['tst_c01']][row['tst_c02']]:
                        raise Exception('Duplicate key for %s.' % str((row['tst_c01'], row['tst_c02'], row['tst_c03'])))
                    else:
                        ret[row['tst_c01']][row['tst_c02']][row['tst_c03']] = row
                else:
                    ret[row['tst_c01']][row['tst_c02']] = {row['tst_c03']: row}
            else:
                ret[row['tst_c01']] = {row['tst_c02']: {row['tst_c03']: row}}

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_singleton0a(p_count: Optional[int]) -> Any:
        """
        Test for designation type singleton0.

        :param int p_count: The number of rows selected.
                            * 0 For a valid test.
                            * 1 For a valid test.
                            * 2 For a invalid test.
                            int(11)

        :rtype: *
        """
        return StaticDataLayer.execute_sp_singleton0("call tst_test_singleton0a(%s)", p_count)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_singleton0a_with_lob(p_count: Optional[int], p_blob: Optional[bytes]) -> Any:
        """
        Test for designation type singleton0 with BLOB..

        :param int p_count: The number of rows selected.
                            * 0 For a valid test.
                            * 1 For a valid test.
                            * 2 For a invalid test.
                            int(11)
        :param bytes p_blob: The BLOB.
                             blob

        :rtype: *
        """
        return StaticDataLayer.execute_sp_singleton0("call tst_test_singleton0a_with_lob(%s, %s)", p_count, p_blob)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_singleton1a(p_count: Optional[int]) -> Any:
        """
        Test for designation type singleton1.

        :param int p_count: The number of rows selected.
                            * 0 For a invalid test.
                            * 1 For a valid test.
                            * 2 For a invalid test.
                            int(11)

        :rtype: *
        """
        return StaticDataLayer.execute_sp_singleton1("call tst_test_singleton1a(%s)", p_count)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def tst_test_singleton1a_with_lob(p_count: Optional[int], p_blob: Optional[bytes]) -> Any:
        """
        Test for designation type singleton1 with BLOB.

        :param int p_count: The number of rows selected.
                            * 0 For a invalid test.
                            * 1 For a valid test.
                            * 2 For a invalid test.
                            int(11)
        :param bytes p_blob: The BLOB.
                             blob

        :rtype: *
        """
        return StaticDataLayer.execute_sp_singleton1("call tst_test_singleton1a_with_lob(%s, %s)", p_count, p_blob)


# ----------------------------------------------------------------------------------------------------------------------
