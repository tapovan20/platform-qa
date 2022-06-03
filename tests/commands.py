#
# =============================================================================================
# IBM Confidential
# © Copyright IBM Corp. 2022
# The source code for this program is not published or otherwise divested of its trade secrets,
# irrespective of what has been deposited with the U.S. Copyright Office.
# =============================================================================================
#

"""
This module contains the commands for smoke test
"""
from tests.expected_output import RBD_IMAGE_NAME,RBD_SNAPSHOT_NAME,RBD_POOL_NAME

SUDO_CEPHADM ="sudo acadia-cephadm shell"

#CEPH_HEALTH
CEPH_VERSION = f"'{SUDO_CEPHADM} -- ceph --version -f json-pretty'"
CEPH_STATUS = f"'{SUDO_CEPHADM} -- ceph -s -f json-pretty'"
CEPH_OSD_LIST_POOLS = f"'{SUDO_CEPHADM} -- ceph osd lspools -f json-pretty'"
CEPH_OSD_DEVICE_CLASS = f"'{SUDO_CEPHADM} -- ceph osd crush class ls -f json-pretty'"
CEPH_OSD_TREE = f"'{SUDO_CEPHADM} -- ceph osd tree -f json-pretty'"

#CEPH PGS_AND _MONS
CEPH_PG_STATS = f"'{SUDO_CEPHADM} -- ceph pg stat -f json-pretty'"
CEPH_MON_STATS = f"'{SUDO_CEPHADM} -- ceph mon stat -f json-pretty'"
CEPH_DF = f"'{SUDO_CEPHADM} -- ceph df -f json-pretty'"
CEPH_OSD_DF = f"'{SUDO_CEPHADM} -- ceph osd df -f json-pretty'"

#CEPH_RBD_IMAGE
CEPH_RBD_LIST_IMAGE = f"'{SUDO_CEPHADM} -- rbd ls {RBD_POOL_NAME}'"
CEPH_RBD_IMAGE_INITIALIZATION = f"'{SUDO_CEPHADM} -- rbd pool init {RBD_POOL_NAME}'"
CEPH_RBD_IMAGE_INFO = f"'{SUDO_CEPHADM} -- rbd info --pool {RBD_POOL_NAME}"\
                      f" --image {RBD_IMAGE_NAME} --format json'"
CEPH_RBD_IMAGE_MAP = f"'{SUDO_CEPHADM} -- rbd map {RBD_IMAGE_NAME} --pool "\
                     f"{RBD_POOL_NAME}'"
CEPH_RBD_SHOW_MAP = f"'{SUDO_CEPHADM} -- rbd showmapped --format json'"
CEPH_RBD_MKFS = f"'sudo mkfs.ext4 -m0 /dev/rbd/{RBD_POOL_NAME}/{RBD_IMAGE_NAME}'"
CEPH_RBD_IMAGE_DISABLE = f"'{SUDO_CEPHADM} -- rbd feature disable {RBD_POOL_NAME}/"\
                         f"{RBD_IMAGE_NAME} object-map fast-diff deep-flatten'"
CEPH_RBD_MOUNT_DIR = f"'sudo mkdir /var/myrbd_mount_{RBD_IMAGE_NAME}'"
CEPH_RBD_MOUNT = f"'sudo mount /dev/rbd/{RBD_POOL_NAME}/{RBD_IMAGE_NAME}"\
                 f" /var/myrbd_mount_{RBD_IMAGE_NAME}'"
CEPH_CREATE_FILE_MP = f"'cd /var/myrbd_mount_{RBD_IMAGE_NAME};sudo truncate "\
                      f"{RBD_IMAGE_NAME}testfile --size 1GB'"
CEPH_DEL_FILE_MP = f"'cd /var/myrbd_mount_{RBD_IMAGE_NAME};sudo rm "\
                   f"{RBD_IMAGE_NAME}testfile'"
CEPH_RBD_IMAGE_CREATE = f"'{SUDO_CEPHADM} -- rbd create -p {RBD_POOL_NAME}"\
                        f" {RBD_IMAGE_NAME} --size 1024'"
CEPH_RBD_IMAGE_RESIZE = f"'{SUDO_CEPHADM} -- rbd resize --pool "\
                        f"{RBD_POOL_NAME} --image  {RBD_IMAGE_NAME} --size 2048'"
CEPH_RBD_LISTING_SNAPSHOT = f"'{SUDO_CEPHADM} -- rbd snap ls --pool {RBD_POOL_NAME}"\
                            f" --image {RBD_IMAGE_NAME} --format json'"
CEPH_RBD_IMAGE_SNAPSHOT_CREATE = f"'{SUDO_CEPHADM} -- rbd snap create {RBD_POOL_NAME}"\
                                 f"/{RBD_IMAGE_NAME}@{RBD_SNAPSHOT_NAME}'"
CEPH_RBD_IMAGE_SNAPSHOT_DEL = f"'{SUDO_CEPHADM} -- rbd snap rm {RBD_POOL_NAME}/"\
                              f"{RBD_IMAGE_NAME}@{RBD_SNAPSHOT_NAME}'"
CEPH_RBD_IMAGE_DEL = f"'{SUDO_CEPHADM} -- rbd rm -p {RBD_POOL_NAME} {RBD_IMAGE_NAME}'"
CEPH_RBD_UNMOUNT_REMOVE = f"'sudo umount /var/myrbd_mount_{RBD_IMAGE_NAME}"\
                          f" -fl;sudo rm -rf /var/myrbd_mount_{RBD_IMAGE_NAME}'"

#CEPH_AUTH_KEYRING
CEPH_CHECK_USER = f"'{SUDO_CEPHADM} -- ceph auth list -f json-pretty'"
CEPH_ADMIN_KEYRING = f"'{SUDO_CEPHADM} -- ceph auth get client.admin -f json-pretty'"
CEPH_AUTOSCALE_MODE = f"'{SUDO_CEPHADM} -- ceph osd pool autoscale-status -f json-pretty'"
DOCKER_CHECK_CONTAINERS = f"'sudo docker ps'"
DOCKER_CHECK_KEY_PROVIDER = f"'sudo docker inspect acadia_key_provider'"
DOCKER_CHECK_ACADIA_CLUSTER_REGISTRATION = f"'sudo docker inspect acadia_cluster_registration'"
DOCKER_CHECK_NODE_EXPORTER = f"'sudo docker inspect node_exporter'"

#CEPH_ENCRYPTION_AT_REST
LIST_DIRECTORIES = f"'sudo ls /var/lib/ceph/'"
CEPH_OSD_STAT = f"'{SUDO_CEPHADM} -- ceph osd stat -f json-pretty'"
CONNECTION_MODE = f"'{SUDO_CEPHADM} -- ceph config get mon ms_client_mode'"


#CEPH_MGR_COMMANDS
CEPH_MGR_STATUS = f"'{SUDO_CEPHADM} -- ceph status -f json-pretty'"
CEPH_MGR_MODULES_LIST= f"'{SUDO_CEPHADM} -- ceph mgr module ls'"
CEPH_MGR_SERVICES= f"'{SUDO_CEPHADM} -- ceph mgr services'"
CEPH_MGR_KEY_CAPS=f"'{SUDO_CEPHADM} -- ceph auth list -f json-pretty'"

#CEPH_ENCRYPTION_IN_TRANSIT
CEPH_MON_DUMP = f"'{SUDO_CEPHADM} -- ceph mon dump --format json-pretty'"
