#
# =============================================================================================
# IBM Confidential
# © Copyright IBM Corp. 2022
# The source code for this program is not published or otherwise divested of its trade secrets,
# irrespective of what has been deposited with the U.S. Copyright Office.
# =============================================================================================
#

import json
import re
from tests.ceph_run import CephRun
from tests.commands import *
from ceph_logger import *
from tests.globals import *
from conftest import confg
from tests.expected_output import *
import pytest

logger = get_logger(__name__)

@pytest.mark.cephmgr
@pytest.mark.smoke
class TestCephMgr(CephRun):
    """class is for testing ceph manager features """

    @pytest.mark.parametrize("command", [(CEPH_MGR_STATUS)])
    def test_ceph_mgr_status(self,command):
        """this test case  check ceph mgr status in Active state or Not
        it will take CEPH_MGR_STATUS command as parameter"""

        logger.info("running ceph mgr status command")
        check_user_output, err = self.run_command(command)
        logger.info("verifying ceph mgr status")
        j_output = json.loads(check_user_output[check_user_output.index('{'):])
        ceph_mgr_status = j_output["mgrmap"]
        try:
            assert ceph_mgr_status["available"] == True, "ceph mgr is in INACTIVE state"
            logger.info("ceph mgr is in ACTIVE state")
        except AssertionError as err:
            logger.error("ceph mgr is in INACTIVE state")
            raise err

    @pytest.mark.parametrize("command", [(CEPH_MGR_MODULES_LIST)])
    def test_ceph_mgr_modules_available(self,command):
        """this test case check all necessary modules are present under always on and enable modules
         it will take CEPH_MGR_MODULES_LIST command as parameter """
        logger.info("running ceph mgr command to list all modules")
        check_user_output, err = self.run_command(command)
        j_output = json.loads(check_user_output[check_user_output.index('{'):])
        ceph_mgr_always_on_modules = j_output["always_on_modules"]
        ceph_mgr_enabled_modules = j_output["enabled_modules"]
        modules_not_enabled=[]
        logger.info("verifying all necessary modules are present under 'always on' lists ")
        try:
            assert ceph_mgr_always_on_modules == Expected_modules, "modules are not present under 'always on' modules list {0}".format(Expected_modules)
            logger.info("All necessary modules are present under 'always on' module list {0}".format(Expected_modules))
        except AssertionError as err:
            logger.error("modules are not present under  always on modules list {0}".format(Expected_modules))
            raise err
        logger.info("verifying all necessary modules are present under 'enable' lists ")
        for module in Enabled_modules:
            try:
                assert module in ceph_mgr_enabled_modules, "{} module is not present under enabled_modules list".format(module)
                logger.info("{} module is present under enabled_modules list".format(module))
            except AssertionError as err:
                logger.error("{} module is not under enabled_modules list".format(module))
                modules_not_enabled.append(module)
        if len(modules_not_enabled):
            raise AssertionError("{} modules are not present in enabled_modules list".format(modules_not_enabled))


    @pytest.mark.parametrize("command", [(CEPH_MGR_SERVICES)])
    def test_ceph_mgr_monitor_services(self,command):
        """this test case check ceph manager display alerting and monitoring service are present or not
         it will take CEPH_MGR_SERVICES command as parameter """
        logger.info("running ceph command to list ceph mgr display alerting and monitoring service")
        check_user_output, err = self.run_command(command)
        j_output = json.loads(check_user_output[check_user_output.index('{'):])
        env=confg.get_env()
        if env["environment"] == "MZONE":
            logger.warning("ceph mgr monitor functionality is not enabled in Mzone ")
        else:
            logger.info("verifying ceph mgr dashboard service")
            ceph_mgr_dashboard_service = j_output["dashboard"]
            ceph_mgr_prometheus_service = j_output["prometheus"]
            try:
                assert ceph_mgr_dashboard_service == self.check_mgr_service(ceph_mgr_dashboard_service), "ceph mgr dashboard service is not working"
                logger.info("verification of ceph mgr dashboard functionality is successful")
            except AssertionError as err:
                logger.error("ceph mgr dashboard service is not working")
                raise err
            try:
                logger.info("verifying ceph mgr prometheus service")
                assert ceph_mgr_prometheus_service == self.check_mgr_service(ceph_mgr_prometheus_service), "ceph mgr prometheus service is not working"
                logger.info("verification of ceph mgr prometheus functionality is successfull")
            except AssertionError as err:
                logger.error("ceph mgr prometheus functionality is unsuccessfull")
                raise err

    @pytest.mark.parametrize("command", [(CEPH_MGR_KEY_CAPS)])
    def test_ceph_mgr_key_caps(self,command):
        """this test case verify the details of keys and caps for ceph manager daemons
        it will take CEPH_MGR_KEY_CAPS command as parameter """
        logger.info("running ceph command to display details of keys and caps for ceph mgr")
        check_user_output, err = self.run_command(command)
        j_output = json.loads(check_user_output[check_user_output.index('{'):])
        ceph_mgr_info = j_output['auth_dump'][-1]
        ceph_mgr_capabilities = ceph_mgr_info["caps"]
        logger.info("verifying keys and caps permissions for ceph mgr ")
        try:
            assert ceph_mgr_capabilities == capabilities and ceph_mgr_info['key'] != None, "ceph mgr not having allow permission in 'mds': 'allow *', 'mon': 'profile mgr', 'osd': 'allow *'"
            logger.info("verification of keys and caps permissions for ceph mgr is successfull")
        except AssertionError as err:
            logger.error("ceph mgr not having allow permission in 'mds': 'allow *', 'mon': 'profile mgr', 'osd': 'allow *'")

    def check_mgr_service(self,service_url):
        """this function checks service url format is correct or not"""
        matched_url = re.search(("((http|https)\:\/\/)?[a-zA-Z0-9\-]+\:[0-9]+\/"), service_url)
        return matched_url.group()
