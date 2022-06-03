#
# =============================================================================================
# IBM Confidential
# © Copyright IBM Corp. 2022
# The source code for this program is not published or otherwise divested of its trade secrets,
# irrespective of what has been deposited with the U.S. Copyright Office.
# =============================================================================================
#

import json
from tests.expected_output import *
from tests.commands import *
from ceph_logger import *
import subprocess
from tests.globals import *
import time
import pytest
from tests.ceph_run import CephRun

logger = get_logger(__name__)

@pytest.mark.rbd
@pytest.mark.smoke
class TestCephRBD(CephRun):
    #listing of rbd libvirt pool
    def listing_rdb_libvirt_pool(self):
        ls, err = self.run_command(CEPH_RBD_LIST_IMAGE)
        return ls

    #used for initializing image
    def initialize_rbd_image(self):
        initialized_image, err = self.run_command(CEPH_RBD_IMAGE_INITIALIZATION)
        logger.info("Image initializing done")
        return initialized_image

    def show_mapped(self):
        try:
            self.run_command(CEPH_RBD_SHOW_MAP)
            logger.info("Show map successful")
        except AssertionError as err:
            logger.error("Show map unsuccessful {}".format(err))


    def make_filesystem(self):
        logger.info("Creating File system")
        rbd_make_fs, err = self.run_command(CEPH_RBD_MKFS)
        time.sleep(10)
        logger.info("Checking if file system is created")
        ls, err = self.listing_of_files("'cd /dev/rbd/libvirt-pool;ls'")
        time.sleep(1)
        try:
            assert (RBD_IMAGE_NAME in ls),'Making file system is unsuccessful'
            logger.info("Making file system is successful")
        except AssertionError as err:
            logger.error("Making file system is unsuccessful")
            raise err

    #used for disabling rbd feature
    def rbd_feature_disable(self):
        try:
            self.run_command(CEPH_RBD_IMAGE_DISABLE)
            logger.info("Featuring disabling is successful for RBD image")
        except AssertionError as err:
            logger.error("Feature disabling is unsuccessful for RBD image")
            raise err


    def listing_of_files(self, command):
        ls,err = self.run_command(command)
        return ls,err



    def create_mount_dir(self):
        logger.info("Creating mount directory ")
        mount_dir, err = self.run_command(CEPH_RBD_MOUNT_DIR)
        logger.info("Checking if mount directory is created")
        ls, err = self.listing_of_files("'cd /var;ls'")
        try:
            assert ("myrbd_mount_" + RBD_IMAGE_NAME in ls),'Failed to create Mount Directory'
            logger.info("Mount directory is created successfully")
        except AssertionError as err:
            logger.error("Mount directory creation is unsuccessful")
            raise err


    #@pytest.mark.parametrize("command", [(CEPH_RBD_MOUNT)])
    def rbd_mount(self):
        logger.info("Creating Mount Path")
        mount_fs, err = self.run_command(CEPH_RBD_MOUNT)
        logger.info("Check Mount Path is Created or not..")
        ls, err = self.listing_of_files("'cd /var;ls'")
        try:
            assert ("myrbd_mount_" + RBD_IMAGE_NAME in ls),'Mount is unsuccessful'
            logger.info("Mount is successful")
        except AssertionError as err:
            logger.error("Mount was unsuccessful")
            raise err


    def create_file_in_mount_path(self):
        logger.info("Creating file in mount path ")
        rbd_file, err = self.run_command(CEPH_CREATE_FILE_MP)
        logger.info("Checking if file is created")
        time.sleep(4)
        ls, err = self.listing_of_files("'"+"cd /var/myrbd_mount_" + RBD_IMAGE_NAME + ";" + "ls"+"'")
        try:
            assert (RBD_IMAGE_NAME + "testfile" in ls),'File creation failed in the mount directory'
            logger.info("File is successfully created in mount directory")
        except AssertionError as err:
            logger.error("File creation is unsuccessful")
            raise err


    def delete_file_mount_path(self):
        logger.info("Deleting file mount directory ")
        rbd_file, err = self.run_command(CEPH_DEL_FILE_MP)
        logger.info("Checking file mount directory is deleted or not")
        ls, err = self.listing_of_files("'"+"cd /var/myrbd_mount_" + RBD_IMAGE_NAME + ";" + "ls"+"'")
        try:
            assert (RBD_IMAGE_NAME + "testfile" not in ls),'testfile delete failed'
            logger.info("File mount directory deletion is successful")
        except AssertioError as err:
            logger.error("File mount directory deletion is unsuccessful")
            raise err

    def rbd_unmapping(self,rbd_mapping):
        command = "'"+SUDO_CEPHADM+" -- rbd unmap -o force "+rbd_mapping+"'"
        rbd_unmapping, err = self.run_command(command)
        if(len(err)>0):
            logger.error("Error in unmapping the device")
        else:
            logger.info("Unmapping the device was successful")


    #@pytest.mark.parametrize("command", [(CEPH_RBD_IMAGE_INFO)])
    def rbd_image_info(self):
        rbd_image_info, err = self.run_command(CEPH_RBD_IMAGE_INFO)
        json_data = json.loads(rbd_image_info)
        return json_data

    def unmount_and_remove_cleanup(self):
        rbd_file, err = self.run_command(CEPH_RBD_UNMOUNT_REMOVE)
        ls, err = self.listing_of_files("'cd /var;ls'")
        try:
            assert ("myrbd_mount_"+RBD_IMAGE_NAME not in ls),'unmount and delete is unsuccessful'
            logger.info("Unmount and cleanup is successful")
        except AssertionError as err:
            logger.info("Unmount and cleanup is unsuccessful")
            raise err

    #Checks if the RBD image is created
    @pytest.mark.parametrize("command", [(CEPH_RBD_IMAGE_CREATE)])
    def test_create_rbd_image(self,command):
        expected_length = len(self.listing_rdb_libvirt_pool())
        logger.info("Creating an RBD image")
        rbd_image_output, err = self.run_command(command)
        logger.info("Image is under creation")
        time.sleep(SLEEP_CONSTANT)
        logger.info("Initializing the image created")
        self.initialize_rbd_image()
        actual_length = len(self.listing_rdb_libvirt_pool())
        try:
            logger.info("Checking if image is created")
            assert (actual_length>expected_length),'Image is not created in the pool, hence not listing'
            logger.info("RBD Image Successfully created")
        except AssertionError as err:
            logger.error("Image is not listing in the pool")
            raise err

    #Checks if the RBD image is resized
    @pytest.mark.parametrize("command", [(CEPH_RBD_IMAGE_RESIZE)])
    def test_resize_rbd_image(self,command):
        ls=self.listing_rdb_libvirt_pool()
        if( RBD_IMAGE_NAME in ls):
            image_info = self.rbd_image_info()
            try:
                assert (image_info[SIZE] == MIN_IMAGE_SIZE or image_info[SIZE] == MAX_IMAGE_SIZE),'Size of the images created are not matching'
                logger.info("Size of the image is 1GiB or 2GiB")
            except AssertionError as err:
                logger.error("Size of the image is not as expected")
                raise err

            image_resize, err = self.run_command(command)
            time.sleep(SLEEP_CONSTANT)
            image_info_2gb = self.rbd_image_info()
            try:
                assert (image_info_2gb[SIZE] == MAX_IMAGE_SIZE),'Resizing of the image failed'
                logger.info("Resizing of the image to 2GB is successful")
            except AssertionError as err:
                logger.error("Resizing of the image failed in except block")
                raise err
        else:
            logger.error(RBD_IMAGE_NAME,"not present in the list")

    #Checks if the RBD mapping is done
    @pytest.mark.parametrize("command", [(CEPH_RBD_IMAGE_MAP)])
    def test_rbd_mapping(self,command):
        self.rbd_feature_disable()
        time.sleep(2)
        rbd_mapping, err = self.run_command(command)
        time.sleep(SLEEP_CONSTANT)
        logger.info("RBD Mapping has started")
        if ('error' not in err):
             logger.info("RBD Mapping is Successful")
        else:
             logger.error("RBD Mapping failed")
        self.show_mapped()
        self.make_filesystem()
        self.create_mount_dir()
        self.rbd_mount()
        self.create_file_in_mount_path()
        self.delete_file_mount_path()
        self.rbd_unmapping(rbd_mapping)
        self.unmount_and_remove_cleanup()
        return rbd_mapping,err

    def listing_of_snapshot(self):
        ls_snap, err = self.run_command(CEPH_RBD_LISTING_SNAPSHOT)
        json_data= json.loads(ls_snap)
        return json_data

    #Checks if the Snapshot is created
    @pytest.mark.parametrize("command", [(CEPH_RBD_IMAGE_SNAPSHOT_CREATE)])
    def test_create_snapshot(self,command):
        snapshot_creation, err = self.run_command(command)
        logger.info("Snapshot under creation")
        time.sleep(SLEEP_CONSTANT)
        snap = self.listing_of_snapshot()
        try:
            logger.info("Verifying if Snapshot is created")
            assert (snap[0]['name'] == RBD_SNAPSHOT_NAME),'Error in creating RBD snapshot'
            logger.info("Verification to create Snapshot is successful")
            self.rbd_image_info()
        except AssertionError as err:
            logger.error("Verification to create Snapshot is unsuccessful")
            raise err

    #Checks if the Snapshot is deleted
    @pytest.mark.parametrize("command", [(CEPH_RBD_IMAGE_SNAPSHOT_DEL)])
    def test_delete_snapshot(self,command):
        deleted_snap, err = self.run_command(command)
        logger.info("Snapshot is deleting")
        time.sleep(SLEEP_CONSTANT)
        snap = self.listing_of_snapshot()
        try:
            logger.info("Verifying if Snapshot is deleted")
            assert (len(snap)==0),'Error in deleting the RBD Snapshot'
            logger.info("Verification to delete the Snapshot is successful")
            self.rbd_image_info()
        except AssertionError as err:
            logger.error("Verification to delete the snapshot is unsuccessful")
            raise err

    #Checks if the RBD image is deleted
    @pytest.mark.parametrize("command", [(CEPH_RBD_IMAGE_DEL)])
    def test_rbd_delete_image(self,command):
        expected_length = len(self.listing_rdb_libvirt_pool())
        deleted_image, err = self.run_command(command)
        logger.info("Image is deleting")
        time.sleep(SLEEP_CONSTANT)
        actual_length = len(self.listing_rdb_libvirt_pool())
        try:
            logger.info("Verifying if image is deleted")
            assert (actual_length<expected_length),'Image deletion failed as length of the actual and expected are not matching'
            logger.info("Verification to delete the Image is successful")
        except AssertionError as err:
            logger.error("Verfication to delete the Image is unsuccessful")
            raise err
