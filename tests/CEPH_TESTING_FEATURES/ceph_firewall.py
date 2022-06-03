#
# =============================================================================================
# IBM Confidential
# © Copyright IBM Corp. 2022
# The source code for this program is not published or otherwise divested of its trade secrets,
# irrespective of what has been deposited with the U.S. Copyright Office.
# =============================================================================================
#

"""
This module will be used to run ceph firewall tests.
"""
import pytest
from tests.ceph_run import CephRun
from ceph_logger import *
from conftest import confg
from tests.globals import *
logger = get_logger(__name__)

@pytest.mark.firewall
@pytest.mark.smoke
class TestCephFirewall(CephRun):
    """
    This class contains test to check Ceph firewall rules and portability.
    """
    def test_accept_rule(self):
        """
        This test function will test if Accept rule is there for other fabric Ips on the listed ports
        """
        input_dic = confg.get_env()
        port_list = Ports.split(" ")
        fabric_ip_list = input_dic["fabric_ip_array"].split(" ")
        logger.info("Checking Accept rule on other node")
        pass_flag = True
        for port in port_list:
            ipts, err = self.run_command("'"+"sudo iptables -nL | grep "+ port+"'")
            iptable_output_list = ipts.split("\n")
            for f_ip in fabric_ip_list:
                count = 0
                for line in iptable_output_list:
                    if f_ip in line and 'ACCEPT' in line:
                        count+=1
                try:
                    assert count == 2,'Failed to verify the rules for '+f_ip
                except AssertionError as err:
                    logger.error('Failed to verify the rules for '+f_ip)
                    pass_flag = False
                    raise err
        if pass_flag:
            logger.info("Verification of Accept rule on other node is successfull")

    def test_portablity_within_range(self):
        """
        This function will test the portability for the port enabled with in range defined.
        """
        logger.info("Checking portability of port")
        input_dic = confg.get_env()
        port_list = Ports.split(" ")
        fabric_ip_list = input_dic["fabric_ip_array"].split(" ")
        st_node_list =input_dic["storage_ip_array"].split(" ")
        pass_flag = True
        if input_dic["storage_ip"] in st_node_list:
            index = st_node_list.index(input_dic["storage_ip"])
        if index ==0:
            for f_ip in fabric_ip_list[1:]:
                for port in port_list:
                    output,err = self.run_command("'"+"echo 'EXIT'| nc "+f_ip+" "+ port+"'")
                    try:
                        assert "ceph" in output, 'Failed to verify the portability for '\
                                             +f_ip+' with '+port
                    except AssertionError as err:
                        logger.error('Failed to verify portability for '+f_ip+" with "+port)
                        pass_flag = False
                        raise err
        elif index in (1,2):
            for f_ip in fabric_ip_list[0:index]+fabric_ip_list[index:]:
                for port in port_list:
                    output,err = self.run_command("'"+"echo 'EXIT'| nc "+f_ip+" "+ port+"'")
                    try:
                        assert  "ceph" in output, 'Failed to verify the portability for '\
                                              +f_ip+' with '+port
                    except AssertionError as err:
                        logger.error('Failed to verify portability for '+f_ip+" with "+port)
                        pass_flag = False
                        raise err
        if pass_flag:
            logger.info("Verification of Portability of Ports is successfull.")
    def test_portability_outside_range(self):
        """
        This test will test the portability is not allowed for the port outside the range defined.
        """
        logger.info("Checking ports should not be enable outside 6800-7300 ")
        input_dic = confg.get_env()
        port_list = Ports.split(" ")
        fabric_ip_list = input_dic["fabric_ip_array"].split(" ")
        st_node_list =input_dic["storage_ip_array"].split(" ")
        pass_flag = True
        if input_dic["storage_ip"] in st_node_list:
            index = st_node_list.index(input_dic["storage_ip"])
        if index ==0:
            for f_ip in fabric_ip_list[1:]:
                port_outside_range =str(int(port_list[-1])-1)
                output,err = self.run_command("'"+"echo 'EXIT'| nc "+f_ip+" "\
                                          + port_outside_range+"'")
                try:
                    assert "ceph" not in output, 'Failed to verify the portability for '+f_ip\
                                             +' with outside port range'
                except AssertionError as err:
                    logger.error('Failed to verify portability for '+\
                                 f_ip+" with outside port range")
                    pass_flag = False
                    raise err
        elif index in (1,2):
            for f_ip in fabric_ip_list[0:index]+fabric_ip_list[index:]:
                port_outside_range =str(int(port_list[-1])-1)
                output,err = self.run_command("'"+"echo 'EXIT'| nc "+f_ip+" "\
                                          + port_outside_range+"'")
                try:
                    assert "ceph" not in output, 'Failed to verify the portability for '+\
                                             f_ip+' with outside port range'
                except AssertionError as err:
                    logger.error('Failed to verify portability for '+f_ip+\
                                 " with outside port range")
                    pass_flag = False
                    raise err
        if pass_flag:
            logger.info("Verification of Ports should not be enable outside 6800-7300 is successfull")
    def test_monitorports_hostip(self):
        """
        This test will test the Monitor port is not enable on HostIps.
        """

        logger.info("Checking port 3300 should not be enable for hostIps")
        input_dic = confg.get_env()
        st_ip =input_dic["storage_ip"]
        output,err = self.run_command("'"+"echo 'EXIT'| nc "+st_ip+" 3300'")
        pass_flag = True
        try:
            assert "ceph" not in output, "Failed to verify that port 3300 is not configured for "+st_ip
        except AssertionError as err:
            logger.error("Failed to verify that port 3300 is not configured for "+st_ip)
            pass_flag = False
            raise err
        if pass_flag:
            logger.info("Verification of Port 3330 not enabled on HostIPs is successfull")