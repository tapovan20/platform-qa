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
from tests.ceph_run import CephRun
from tests.commands import *
from ceph_logger import *
import subprocess
from tests.globals import *
import pytest

logger = get_logger(__name__)

@pytest.mark.keyring
@pytest.mark.smoke
class TestCephKeyring(CephRun):

    #Checks if user key is present
    @pytest.mark.parametrize("command", [(CEPH_CHECK_USER)])
    def test_userkey_generated(self,command):
        #Fetch Output
        logger.info("Checking every OSD has a key")
        check_user_output, err = self.run_command(command)
        j_output = json.loads(check_user_output[check_user_output.index('{'):])
        for i in range(len(j_output['auth_dump'])):
            if j_output['auth_dump'][i]['key'] != None:
                if i==len(j_output['auth_dump'])-1:
                    logger.info("Verifying every OSD has a Key generated is successful")
            else:
                logger.error("Verifying key value is not generated for OSD",j_output['auth_dump'][i]['entity'])

    #Checks if 'client.admin key' is present
    @pytest.mark.parametrize("command", [(CEPH_ADMIN_KEYRING)])
    def test_admin_keyring_generated(self,command):
        #Fetch Output
        logger.info("Checking for admin keyring")
        keyring_output, err = self.run_command(command)
        j_output = json.loads(keyring_output)
        for i in range(len(j_output)):
            try:
                logger.info("Checking if admin KeyRing is present")
                assert (j_output[i]['key'] != None),'Checking the KeyRing present has failed'
                logger.info("Verification if admin KeyRing present is successful")
            except AssertionError as err:
                logger.error("Verification if admin KeyRing is present is unsuccessful")
                raise err


    #Checks if the Auto scalar is in OFF state
    @pytest.mark.parametrize("command", [(CEPH_AUTOSCALE_MODE)])
    def test_autoscaler_state(self,command):
        autoscale_mode, err = self.run_command(command)
        j_output = json.loads(autoscale_mode[autoscale_mode.index('['):])
        pool_list=[]
        for i in range(len(j_output)):
            try:
                logger.info("Checking the autoscale mode")
                assert (j_output[i]['pg_autoscale_mode'] == "off"),\
                    'pg_autoscale_mode is expected to be in off state but Autoscale mode is ON in pool'
                logger.info("Verification of the autoscale mode is successful")
            except AssertionError as err:
                logger.error("Verification of autoscale mode is unsuccessful-Autoscale mode is ON in pool")
                raise err

    #Checks if all the necessary containers are present
    @pytest.mark.parametrize("command", [(DOCKER_CHECK_CONTAINERS)])
    def test_necessary_containers_presence(self, command):
        logger.info("Grabbing command - {} to get the list of services".format(command))
        docker_ps_output, err = self.run_command(command)
        logger.info("checking if {} are present".format(CONTAINERISED_SERVICES_LIST))
        for container in CONTAINERISED_SERVICES_LIST:
            try:
                assert (container in docker_ps_output), '{} is not present'.format(container)
                logger.info("verification of {} presence is successful".format(container))
            except AssertionError as err:
                logger.error("verification of {} presence is unsuccessful".format(container))
                raise err


    #Checks if Acadia Key Provider service is Running and Healthy
    @pytest.mark.parametrize("command", [(DOCKER_CHECK_KEY_PROVIDER)])
    def test_keyprovider_health_and_state(self,command):
        logger.info("Grabbing command - {} to check acadia_key_provider state & health".format(command))
        docker_inspect_output, err = self.run_command(command)
        j_output = json.loads(docker_inspect_output[
                              docker_inspect_output.index("[") + 1:docker_inspect_output.rindex("]")])
        # checking state
        try:
            logger.info("Checking Key provider state")
            state = j_output["State"]["Status"]
            assert (state == "running"), \
                'Acadia-key-provider is not in running state or {}'.format(err)
            logger.info("Verification of Acadia-key-provider state is successful")
        except KeyError as err:
            logger.error("KeyError : {}".format(err))
            raise err
        except AssertionError as err:
            logger.error("Verification of Acadia-key-provider state is unsuccessful err : {}".format(err))
            raise err

        # checking health status
        try:
            logger.info("checking for key provider health")
            health_state = j_output["State"]["Health"]["Status"]
            assert health_state == "healthy", 'key provider is in {} state'.format(health_state)
            logger.info("Key Provider is in healthy state")
        except KeyError as err:
            logger.error("KeyError : {}".format(err))
            raise err
        except AssertionError as err:
            logger.error("key provider health check is unsuccessful")
            raise err

    #Checks if Acadia cluster registration service is Running and healthy
    @pytest.mark.parametrize("command", [(DOCKER_CHECK_ACADIA_CLUSTER_REGISTRATION)])
    def test_registration_server_health_and_state(self,command):
        logger.info("Grabbing command - {} to check acadia_cluster_registration status & health".format(command))
        docker_inspect_output, err = self.run_command(command)
        j_output = json.loads(docker_inspect_output[
                              docker_inspect_output.index("[") + 1:docker_inspect_output.rindex("]")])
        # checking state
        try:
            logger.info("Checking acadia-registration-server state")
            state = j_output["State"]["Status"]
            assert (state == "running"), \
                'Acadia-registration-server is not in running state or {}'.format(err)
            logger.info("Acadia-registration-server is in running state")
        except KeyError as err:
            logger.error("KeyError : {}".format(err))
            raise err
        except AssertionError as err:
            logger.error("Verification of Acadia-registration-server state is unsuccessful err : {}".formar(err))
            raise err

        # checking health status
        try:
            logger.info("checking for Acadia-registration-server health")
            health_state = j_output["State"]["Health"]["Status"]
            assert health_state == "healthy", 'Acadia-registration-server is in {} state'.format(health_state)
            logger.info("Acadia-registration-server is in healthy state")
        except KeyError as err:
            logger.error("KeyError : {}".format(err))
            raise err
        except AssertionError as err:
            logger.error("Acadia-registration-server health check is unsuccessful err: {}".format(err))
            raise err


    #checks if node exporter service is RUNNING
    @pytest.mark.parametrize("command", [(DOCKER_CHECK_NODE_EXPORTER)])
    def test_nodeexporter_state(self,command):
        logger.info("Grabbing command - {} to check node_exporter state".format(command))
        docker_inspect_output, err = self.run_command(command)
        j_output = json.loads(docker_inspect_output[
                              docker_inspect_output.index("[") + 1:docker_inspect_output.rindex("]")])
        try:
            logger.info("Checking the node exporter state")
            state = j_output["State"]["Status"]
            assert (state == "running"),\
                ' Node Exporter is in stopped state or {}'.format(err)
            logger.info("Node exporter is in running state ")
        except KeyError as err:
            logger.error("KeyError : {}".format(err))
            raise err
        except AssertionError as err:
            logger.error("Verification on Node Exporter state is unsuccessful err : {}".format(err))
            raise err

