#
# =============================================================================================
# IBM Confidential
# © Copyright IBM Corp. 2022
# The source code for this program is not published or otherwise divested of its trade secrets,
# irrespective of what has been deposited with the U.S. Copyright Office.
# =============================================================================================
#

import json
from tests.ceph_run import CephRun
from tests.expected_output import *
from ceph_logger import *
from tests.globals import *
from tests.commands import *
import subprocess
import pytest

logger = get_logger(__name__)

@pytest.mark.health
@pytest.mark.smoke
class TestCephHealth(CephRun):
    @pytest.mark.parametrize("command", [(CEPH_VERSION)])
    # Checks if Ceph version is matching the expected version
    def test_ceph_version(self, command):
        logger.info("Verify Version ID and Version state")
        ceph_version, err = self.run_command(command)
        list_ceph_version = ceph_version.split()
        actual_version = list_ceph_version[2]
        actual_state = list_ceph_version[5]
        try:
            logger.info("Checking Version ID")
            assert VERSION_ID == actual_version, 'VERSION_ID expected is '+VERSION_ID+' but got '+actual_version
            logger.info("Verification of the Version ID is successful")
        except AssertionError as err:
            logger.error("Verification of Version ID is unsuccessful")
            raise err

        try:
            logger.info("Checking the Ceph State")
            assert VERSION_STATE == actual_state, 'State of the ceph expected is '+VERSION_STATE+' but got ' +actual_state
            logger.info("Verification of Ceph state is successful")
        except AssertionError as err:
            logger.error("Verification of Ceph state is unsuccessful")
            raise err


    @pytest.mark.parametrize("command", [(CEPH_STATUS)])
    # Checks if Ceph health status is 'OK'
    def test_ceph_status(self, command):
        # Fetch output
        logger.info("Verify the Ceph status")
        ceph_status, err = self.run_command(command)
        json_data = json.loads(ceph_status)
        status = json_data[HEALTH][STATUS]
        total_osds, total_up_osds, total_in_osds = json_data[OSDMAP][NUM_OSDS], json_data[OSDMAP][NUM_UP_OSDS],json_data[OSDMAP][NUM_IN_OSDS]
        try:
            logger.info("Checking the status")
            assert ((status == HEALTHOK or status == HEALTHWARN) and (total_osds == total_up_osds == total_in_osds)), 'Expecting Health of the CEPH status in OK or WARN state'
            logger.info("Verification of the status successfully")
        except AssertionError as err:
            logger.error("Verification of the Status is unsuccessful")
            raise err


    @pytest.mark.parametrize("command", [(CEPH_OSD_LIST_POOLS)])
    # Checks if Ceph both the pools are present [device_health_metrics and libvirt-pool]
    def test_count_osd_pools(self, command):
        # Fetch output
        logger.info("Verify the count of the OSD pools")
        ceph_pools, err = self.run_command(command)
        json_data = json.loads(ceph_pools)
        actual_pools = [str(i[POOLNAME]) for i in json_data]
        try:
            logger.info("Checking the count of OSD POOLS")
            assert (set(POOLS).issubset(set(actual_pools))), 'Expecting list of pools are not matching'
            logger.info("Verification of the OSD  pools successful")
        except AssertionError as err:
            logger.error("Verification of the OSD pools is unsuccessful")
            raise err



    @pytest.mark.parametrize("command", [(CEPH_OSD_DEVICE_CLASS)])
    # Checks if the device class is present [HDD/SDD]
    def test_device_class_present(self, command):
        # Fetch output
        logger.info("Verify the Device class")
        ceph_device_class, err = self.run_command(command)
        json_data = json.loads(ceph_device_class)
        try:
            logger.info("Checking  the Device class")
            assert (set(json_data) == set(DEVICE_CLASS)), 'Expecting Device_class and actual Device_class are different'
            logger.info("Verification of  the Device class successfully")
        except AssertionError as err:
            logger.error("Verification of the Device class is unsuccessful")
            raise err


    @pytest.mark.parametrize("command", [(CEPH_OSD_TREE)])
    # Check if OSDs are UP and its weight is 1
    def test_osd_status_and_reweight(self, command):
        # Fetch output
        logger.info("Verify the OSD tree info")
        ceph_osd_tree, err = self.run_command(command)
        json_data = json.loads(ceph_osd_tree)
        for osd in json_data[NODES]:
            try:
                if osd[ID] < 0:
                    continue
                else:
                    logger.info("Checking the OSD{} info".format(osd[ID]))
                    assert (osd[STATUS] == UP and osd[REWEIGHT] == REWEIGHT_VALUE), 'Expecting the osd{}_status to be UP and_reweight to be 1.0'.format(osd[ID])
                    logger.info("Verification of  OSD{} info is successful".format(osd[ID]))
            except AssertionError as err:
                logger.error("Verification of OSD{} info is unsuccessful".format(osd[ID]))
                raise err
