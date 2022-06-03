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


@pytest.mark.encryption
@pytest.mark.smoke
class TestEncryptionAtRestLockBoxKeying(CephRun):
    @pytest.mark.parametrize("command", [(LIST_DIRECTORIES)])
    def test_osd_lockbox_keyring(self, command):
        logger.info("List All Directories inside CEPH folder and select directory which have all OSD's")
        output, err = self.run_command(command)
        list_directory = output.split('\n')
        directory = [i for i in list_directory if len(i) == 36]
        self.enter_directory(directory[0])

    def enter_directory(self, directory):
        command = "'sudo ls /var/lib/ceph/" + directory + " | grep osd'"
        all_osd, err = self.run_command(command)
        osd_list = all_osd.split('\n')
        logger.info("Check lockbox keyring key for each OSD via filesystem method")
        for osd_id in osd_list[0:len(osd_list) - 1]:
            self.lockbox_keyring_via_filesystem(directory, osd_id)
        logger.info("Check lockbox keyring key for each OSD via ceph volume method")
        for osd_id in osd_list[0:len(osd_list) - 1]:
            self.lockbox_keyring_via_ceph_volume(osd_id)

    def lockbox_keyring_via_filesystem(self, directory, osd_id):
        command = "'sudo cat /var/lib/ceph/" + directory + "/" + osd_id + "/lockbox.keyring | grep key'"
        encryption_key, err = self.run_command(command)
        data1 = encryption_key.strip("\t\n").split(" = ")
        try:
            assert len(data1) == 2 and data1[1] != None, "{} lockbox keyring is not present and OSD is not Encrypted".format(osd_id)
            logger.info("{} lockbox keyring is present and OSD is encrypted".format(osd_id))
        except AssertionError as err:
            logger.error("{} lockbox keyring is not present and OSD is not Encrypted".format(osd_id))
            raise err

    def lockbox_keyring_via_ceph_volume(self, osd_id):
        command = "'"+SUDO_CEPHADM+" -- ceph-volume lvm list 2>/dev/null | grep -w \"====== " + osd_id + " ======\" -A 17 | grep cephx'"
        cephx_lockbox_key, err = self.run_command(command)
        data1 = cephx_lockbox_key.strip().split("secret")
        try:
            assert len(data1) == 2 and data1[1] != None, "{} lockbox keyring is not present and OSD is not Encrypted".format(osd_id)
            logger.info("{} lockbox keyring is present and OSD is encrypted".format(osd_id))
        except AssertionError as err:
            logger.error("{} lockbox keyring is not present and OSD is not Encrypted".format(osd_id))
            raise err


@pytest.mark.smoke
class TestEncryptionAtRestDmcryptKey(CephRun):
    @pytest.mark.parametrize("command", [(CEPH_OSD_STAT)])
    def test_check_dmcrypt_key(self, command):
        output, err = self.run_command(command)
        json_data = json.loads(output)
        numberOfOsd = json_data['num_osds']
        for osd_num in range(numberOfOsd):
            self.getOSD_FSID(str(osd_num))

    def getOSD_FSID(self, osd_num):
        command = "'"+SUDO_CEPHADM+" -- ceph osd find " + osd_num + " -f json-pretty'"
        osd_info, err = self.run_command(command)
        json_data = json.loads(osd_info)
        osd_id = "osd " + str(json_data['osd'])
        osd_fsid = json_data['osd_fsid']
        self.get_dmcrypt_key(osd_fsid, osd_id)

    def get_dmcrypt_key(self, osd_fsid, osd_id):
        command = "'"+SUDO_CEPHADM+" -- ceph config-key get dm-crypt/osd/" + osd_fsid + "/luks && echo'"
        dmcrypt_key, err = self.run_command(command)
        try:
            assert dmcrypt_key != None, "for {} dmcrypt key is not present and osd is encrypted".format(osd_id)
            assert len(dmcrypt_key) == 173, "for {} excepted dmcrypt key length is 173  but got {}".format(osd_id,len(dmcrypt_key))
            logger.info("for {} dmcrypt key is present and osd is encrypted".format(osd_id))

        except AssertionError as err:
            logger.error("for {} dmcrypt key is not present and osd is not encrypted".format(osd_id))
            raise err

    @pytest.mark.parametrize("command", [(CONNECTION_MODE)])
    def test_crc_secure_connection_mode(self, command):
        connection_mode, err = self.run_command(command)
        try:
            assert connection_mode.strip('\n') == "secure", "connection not enbled with secure mode"
            logger.info("The connection is enabled with secure mode")
        except AssertionError as err:
            logger.error("connection not enbled with secure mode ")
            raise err
            
    @pytest.mark.parametrize("command", [(CEPH_MON_DUMP)])
    def test_encryption_at_transit(self, command):
        messengerV2, err = self.run_command(command)
        json_data=json.loads(messengerV2)
        logger.info("Checking encryption at transit on acadia platform")
        for stgr_nodes in json_data['mons']:
            strg_node = (stgr_nodes['name'])
            port_type,port_addr=[],[]
            for ports in stgr_nodes['public_addrs']['addrvec']:
                port_type.append(ports['type'])
                port_addr.append(ports['addr'].split(':')[1])
            try:
                assert 'v2' in port_type and '3300' in port_addr, "Messenger V2 port is not enabled on storage node {}".format(strg_node)
                logger.info("Messenger V2 port has enabled on storage node {}".format(strg_node))
            except AssertionError as err:
                logger.error("Messenger V2 port is not enabled on storage node {}".format(strg_node))
                raise err
