#
# =============================================================================================
# IBM Confidential
# © Copyright IBM Corp. 2022
# The source code for this program is not published or otherwise divested of its trade secrets,
# irrespective of what has been deposited with the U.S. Copyright Office.
# =============================================================================================
#

'''Import necessary modules'''
# Import required modules
import logging
import requests
from OUT import MASTER_IP  # pylint: disable=E0401

# logging info
logging.basicConfig(filename='/tmp/zabbix.log',
                    format='%(asctime)s : %(message)s',
                    filemode='w', level=logging.DEBUG)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# add the handler to the root logger
logging.getLogger('').addHandler(console)

UNAME = "Admin"
PWORD = "zabbix"
TEMPLATE_NAME = "Linux by Zabbix agent"
HOST_GROUP_NAME = "Templates/Operating systems"
ZABBIX_API_URL = "http://"+MASTER_IP+":8080/api_jsonrpc.php"


token = {
    "jsonrpc": "2.0",
    "method": "user.login",
    "params": {
          "user": UNAME,
          "password": PWORD},
    "id": 1
     }

# Token generation
logging.info('Authentication token to be generated')
try:
    get_token = requests.post(ZABBIX_API_URL, json=token)
    AUTHTOKEN = get_token.json()["result"]
    logging.info('Authentication token is generated successfully')
except AssertionError as err:
    logging.error("Generation of token \
            failed".format(err))  # pylint: disable=W1202,C0209,W1310
