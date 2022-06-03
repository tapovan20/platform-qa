#
# =============================================================================================
# IBM Confidential
# © Copyright IBM Corp. 2022
# The source code for this program is not published or otherwise divested of its trade secrets,
# irrespective of what has been deposited with the U.S. Copyright Office.
# =============================================================================================
#

'''This file calls all the features class'''
from tests.CEPH_TESTING_FEATURES.ceph_encryption import \
        TestEncryptionAtRestLockBoxKeying, TestEncryptionAtRestDmcryptKey
from tests.CEPH_TESTING_FEATURES.ceph_health import TestCephHealth
from tests.CEPH_TESTING_FEATURES.ceph_pool import \
        TestCephPoolPGandOSDs
from tests.CEPH_TESTING_FEATURES.ceph_rbd import TestCephRBD
from tests.CEPH_TESTING_FEATURES.ceph_keyring import TestCephKeyring
from tests.CEPH_TESTING_FEATURES.ceph_mgr import TestCephMgr
from tests.CEPH_TESTING_FEATURES.ceph_firewall import TestCephFirewall

ceph_health = TestCephHealth()
ceph_pools = TestCephPoolPGandOSDs()
ceph_rbd = TestCephRBD()
ceph_keyring = TestCephKeyring()
ceph_encryption = TestEncryptionAtRestLockBoxKeying()
ceph_encryption = TestEncryptionAtRestDmcryptKey()
ceph_mgr = TestCephMgr()
ceph_firewall = TestCephFirewall()