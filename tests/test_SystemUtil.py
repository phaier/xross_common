# -*- coding: utf-8 -*-
""" TestSystemUtil """
import os
import sys
import unittest  # @unittest annotation needs this import.

from xross_common.SystemLogger import SystemLogger
from xross_common.SystemUtil import SystemUtil, SystemEnv
from xross_common.XrossTestBase import XrossTestBase

TEST_KEY_PARAM = "TEST_KEY"
TEST_VALUE_PARAM = "TEST_VALUE"


class TestSystemUtil(XrossTestBase):
    logger, test_handler = SystemLogger("TestSystemUtil").get_logger()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cfg = SystemUtil()

    def test_show_sysprop(self):
        self.cfg.clear_gcfg_for_test()
        self.assertEqual("Munch({})", str(self.cfg.get_all_sysprop()))

    def test_set_sysprop(self):
        # setup
        self.sysprop = self.cfg.get_all_sysprop()

        # action
        self.cfg.set_sysprop(TEST_KEY_PARAM, TEST_VALUE_PARAM)

        # assert
        self.assertEqual(TEST_VALUE_PARAM, self.sysprop[TEST_KEY_PARAM])

    def test_get_sysprop(self):
        # setup
        self.test_set_sysprop()

        # action/assert
        self.assertEqual(TEST_VALUE_PARAM, self.cfg.get_sysprop(TEST_KEY_PARAM))

    def test_set_get_sysprop_dict(self):
        # setup
        TEST_KEY_PARAM_DICT = "FRASHCRASHER_1.DELTA_PRICE"
        TEST_VALUE_PARAM_DICT = "{'MCO/BTC':0.00002,'BNB/BTC':0.000001}"
        self.sysprop = self.cfg.get_all_sysprop()

        # action
        self.cfg.set_sysprop(TEST_KEY_PARAM_DICT, TEST_VALUE_PARAM_DICT)

        # assert
        self.assertEqual(TEST_VALUE_PARAM_DICT, self.sysprop[TEST_KEY_PARAM_DICT])

        # action/assert
        self.assertEqual({'MCO/BTC': 0.00002, 'BNB/BTC': 0.000001}, self.cfg.get_sysprop(TEST_KEY_PARAM_DICT, type=dict))

    def test_set_get_sysprop_pack(self):
        # setup
        TEST_KEY_PARAM_PACK = "FRASHCRASHER_1.INTERVALS"
        TEST_VALUE_PARAM_PACK = "5,1"
        self.sysprop = self.cfg.get_all_sysprop()

        # action
        self.cfg.set_sysprop(TEST_KEY_PARAM_PACK, TEST_VALUE_PARAM_PACK)

        # assert
        self.assertEqual(TEST_VALUE_PARAM_PACK, self.sysprop[TEST_KEY_PARAM_PACK])

        # action/assert
        self.assertEqual(['5', '1'], self.cfg.get_sysprop(TEST_KEY_PARAM_PACK, type=dict))

    def test_remove_sysprop(self):
        self.test_get_sysprop()

        # action/teardown
        self.cfg.remove_sysprop(TEST_KEY_PARAM)

        # teardown
        with self.assertRaises(KeyError):
            expected_none = self.sysprop[TEST_KEY_PARAM]
            self.assertEqual(None, expected_none)
            self.fail()

    def test_set_env(self):
        # action
        self.cfg.set_env(TEST_KEY_PARAM, TEST_VALUE_PARAM)

        # assert
        self.assertEqual(TEST_VALUE_PARAM, os.environ.get(TEST_KEY_PARAM))

    def test_get_env(self):
        # setup
        self.test_set_env()

        # action/assert
        self.assertEqual(TEST_VALUE_PARAM, self.cfg.get_env(TEST_KEY_PARAM))

    def test_get_env_from_setenvsh(self):
        # assert
        self.assertFalse(None, self.cfg.get_env("DOCKER_DIST_DIR"))
        self.assertFalse("", self.cfg.get_env("DOCKER_DIST_DIR"))

    def test_remove_env(self):
        # setup
        self.test_get_env()

        # action/teardown
        self.cfg.remove_env(TEST_KEY_PARAM)

        # assert
        self.assertEqual(None, os.environ.get(TEST_KEY_PARAM))

    def test_read_config(self):
        # assert
        self.assertEqual("True", self.cfg.get_sysprop_or_env('TEST_READ_CONFIG'))
        self.assertTrue(self.cfg.get_sysprop_or_env('TEST_READ_CONFIG', type=bool))
        self.assertEqual("True", self.cfg.get_sysprop("TEST_SYSTEM_UTIL.READ_CONFIG"))
        self.assertTrue(self.cfg.get_sysprop("TEST_SYSTEM_UTIL.READ_CONFIG", type=bool))

    # MEMO: confirming extra picture with the bottom code enabled
    def test_sys_args_and_env(self):
        print("=======ENVIRONMENT VARIABLES========")
        # print(self.cfg.get_all_env_for_test()) # not to show SECRET_KEY in log
        print("=======SYSPROP========")
        print(sys.argv[1:])
        print("config.ini and sys.argv[1:] contains " + str(len(self.cfg.get_all_sysprop())))

    def test_system_env(self):
        self.logger.info("SystemEnv is " + str(self.cfg.env))
        self.logger.info("IS_LOCAL : " + str(self.cfg.env.is_local()))
        self.logger.info("IS_DOCKER : " + str(self.cfg.env.is_docker()))
        self.logger.info("IS_UNITTEST : " + str(self.cfg.env.is_unittest()))
        self.assertFalse(self.cfg.env.is_real())
        self.assertNotEqual(SystemEnv.UNKNOWN, self.cfg.env)


if __name__ == '__main__':
    TestSystemUtil.do_test()
    # TestSystemUtil().test_sys_args() # if you try test_sys_args, this line should be uncommented.