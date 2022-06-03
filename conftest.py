#
# =============================================================================================
# IBM Confidential
# © Copyright IBM Corp. 2022
# The source code for this program is not published or otherwise divested of its trade secrets,
# irrespective of what has been deposited with the U.S. Copyright Office.
# =============================================================================================
#

'''This is a file to get the final results '''
import json
import time
from _pytest.terminal import TerminalReporter  # pylint: disable=unused-import
import pytest

class confg:  # pylint: disable=C0103
    # pylint: disable=R0903
    '''This class is to set up the environment and storagenode ip '''
    def __init__(self):
        self.env = ""
        self.storage_ip = ""
        self.fabric_ip_array = ""
    def get_env():  # pylint: disable=E0211
        '''This function is to get the environment '''
        get_env_dict = {}
        get_env_dict['environment'] = confg.env
        get_env_dict['storage_ip'] = confg.storage_ip
        get_env_dict['fabric_ip_array'] = confg.fabric_ip_array
        get_env_dict['storage_ip_array'] = confg.storage_ip_array
        return get_env_dict


def pytest_addoption(parser):
    '''This function is to set the environment and the storage node ip'''
    parser.addoption("--env", action="store", default=None, help="provide env VE or Mzone")  # nopep8 # pylint: disable=C0301
    parser.addoption("--storage_ip", action="store", default=None, help="provide stg ip")  # nopep8
    parser.addoption("--fabric_ip_array", action="store", default=None, help="provide Fabric IP array")  # nopep8
    parser.addoption("--storage_ip_array", action="store", default=None, help="ports_array") #nopep8

@pytest.fixture(scope="session", autouse=True)
def setup(request):
    '''This function is to set up the config of environment and storage node ip as fixture'''  # nopep8 # pylint: disable=C0301
    confg.env = request.config.getoption("--env")
    confg.storage_ip = request.config.getoption("--storage_ip")
    confg.fabric_ip_array = request.config.getoption("--fabric_ip_array")
    confg.storage_ip_array =  request.config.getoption("--storage_ip_array")
def pytest_terminal_summary(terminalreporter):
    ''' This function gets the summary of the tests run '''
    results = {}
    if 'passed' in terminalreporter.stats:
        results["PASS"] = len(terminalreporter.stats['passed'])
    else:
        results["PASS"] = 0
    if 'failed' in terminalreporter.stats:
        results["FAIL"] = len(terminalreporter.stats['failed'])
    else:
        results["FAIL"] = 0
    if 'deselected' in terminalreporter.stats:
        results["SKIP"] = len(terminalreporter.stats['deselected'])
    else:
        results["SKIP"] = 0
    # pylint: disable=W0212
    duration = time.time() - terminalreporter._sessionstarttime
    results["ELAPSED_TIME"] = duration
    with open('ceph_smoke_logfiles/CEPH_smoke_test_results.json', 'w', encoding="UTF-8") as t_res:  # nopep8 # pylint: disable=C0301
        json.dump(results, t_res, indent=4)