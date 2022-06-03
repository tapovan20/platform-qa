#
# =============================================================================================
# IBM Confidential
# © Copyright IBM Corp. 2022
# The source code for this program is not published or otherwise divested of its trade secrets,
# irrespective of what has been deposited with the U.S. Copyright Office.
# =============================================================================================
#

''' Import all required modules '''
import json
import logging
import requests  # pylint: disable=C0303
from OUT import *  # pylint: disable=E0401,W0401
from generate_token import *  # pylint: disable=E0401,W0401,W0614
from payload import *  # pylint: disable=E0401,W0401,W0614

# pylint: disable=C0116,C0103,W1202,W0602,W1310
# pylint: disable=C0209,W0612
# pylint: disable=redefined-outer-name


def test_to_get_host_id():
    try:
        global host_id  # pylint: disable=C0103
        logging.info('To get the Host and Host ID details')
        req_host_id = requests.post(ZABBIX_API_URL,
                                    json=host_id)
        Host_id = json.dumps(req_host_id.json(), indent=4, sort_keys=True)
        logging.info('Got Host and Host_ID Successfully')
    except AssertionError as err:
        logging.error("Getting host ID failed".format(err))


def test_to_check_host_status():
    try:
        global host_status
        logging.info('Checking the host status present in the cluster')
        req_host_status = requests.post(ZABBIX_API_URL,
                                        json=host_status)
        host_info = json.dumps(req_host_status.json(),
                               indent=4, sort_keys=True)
        Host_status = json.loads(host_info)
        # Getting status of each host
        host_1 = Host_status["result"][0]["status"]
        host_2 = Host_status["result"][1]["status"]
        host_3 = Host_status["result"][2]["status"]
        # Checking host status of all host
        assert (host_1 and host_2 and host_3 == '0'), "Host\
                status check failed"
        logging.info('Got Host status Successfully')
    except AssertionError as err:
        logging.error("Getting host status failed".format(err))


def test_to_get_hostgroup():
    try:
        global host_group
        logging.info('To get Hostgroup ID')
        req_hostgroup_get = requests.post(ZABBIX_API_URL,
                                          json=host_group)
        Host_group = json.dumps(req_hostgroup_get.json(),
                                indent=4, sort_keys=True)
        logging.info('got details of Hostgroup ID successfully')
    except AssertionError as err:
        logging.error("Getting hostgroup ID failed".format(err))


test_to_get_host_id()
test_to_check_host_status()
test_to_get_hostgroup()

try:
    logging.info('User to be logged out')
    logout = requests.post(ZABBIX_API_URL,
                           json=logout)
    logging.info('User logout successful')
except AssertionError as err:
    logging.error("Logging out failed".format(err))\
            # pylint: disable=W1202,C0209,W1310
