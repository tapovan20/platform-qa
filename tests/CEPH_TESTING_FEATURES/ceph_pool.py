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
import subprocess
from tests.globals import *
from tests.commands import *
import pytest

logger = get_logger(__name__)

@pytest.mark.pool
@pytest.mark.smoke
class TestCephPoolPGandOSDs(CephRun):
    # Checks if all the PGs state is 'active+clean'
    @pytest.mark.parametrize("command", [(CEPH_PG_STATS)])
    def test_pg_state(self, command):
        # Fetch output
        logger.info("Checking PG stats")
        pgs, err = self.run_command(command)
        json_data = json.loads(pgs)
        keys_to_assert = json_data[PG_SUMMARY][NUM_PG_BY_STATE]
        try:
            logger.info("Verifying the details for PG stats")
            assert keys_to_assert[0][NAME] == PG_STATUS, 'Failed to show details about the pg stats'
            logger.info("Verification for PG stats is successful")
        except AssertionError as err:
            logger.error("Verification for PG stats is unsuccessful")
            raise err

    # Checks if the ceph monitors are present on different nodes
    @pytest.mark.parametrize("command", [(CEPH_MON_STATS)])
    def test_mon_count(self,command):
        # Fetch output
        logger.info("Checking monitor stats")
        mons, err = self.run_command(command)
        json_data = json.loads(mons)
        key_to_assert = json_data[NUM_MONS]
        try:
            logger.info("Checking monitor stats are matching to key to asserts")
            assert key_to_assert == MAX_MONS, 'Key to assert and maximum monitor are not matching'
            logger.info("Verification for mon stats is successful")
        except:
            logger.error("Verification for mon stats is unsuccessful")
            raise err

    # Checks if the OSD utilization% is NOT greater than 75
    @pytest.mark.parametrize("command", [(CEPH_DF)])
    def test_osd_utilization_percentage(self, command):
        logger.info("Checking Ceph df")
        ceph_df, err = self.run_command(command)
        json_data = json.loads(ceph_df)
        key_to_assert = json_data[STATS_BY_CLASS][DEVICE_CLASS[0]][TOTAL_USED_RAW_RATIO]
        rawdataused = round((key_to_assert * 100), 2)
        try:
            logger.info("Verifying while using Ceph df command")
            assert (rawdataused < MAX_UTILIZATION),'Failed while check the CEPH df command'
            logger.info("Verification for ceph df is successful")
        except AssertionError as err:
            logger.error("Verification for ceph df is unsuccessful")
            raise err

    # Checks if the Ceph total raw storage used is NOT greater than 75
    @pytest.mark.parametrize("command", [(CEPH_OSD_DF)])
    def test_ceph_raw_storage_used(self, command):
        logger.info("Checking OSD df")
        osd_df, err = self.run_command(command)
        json_data = json.loads(osd_df)
        for osd in json_data[NODES]:
            try:
                logger.info("Verifying OSD{} df".format(osd[ID]))
                assert (osd[UTILIZATION] < MAX_UTILIZATION), 'Failed while checking OSD df command'
                logger.info('Verification for OSD{} df is successful'.format(osd[ID]))
            except AssertionError as err:
                logger.info("Verification for OSD{} df is unsuccessful".format(osd[ID]))
                raise err