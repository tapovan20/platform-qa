#
# =============================================================================================
# IBM Confidential
# © Copyright IBM Corp. 2022
# The source code for this program is not published or otherwise divested of its trade secrets,
# irrespective of what has been deposited with the U.S. Copyright Office.
# =============================================================================================
#

''' Import required modules '''
from OUT import HOST_1, HOST_2, HOST_3  # pylint: disable=E0401,W0401
from generate_token import AUTHTOKEN, HOST_GROUP_NAME  # pylint: disable=W0401
# pylint: disable=E0602,W0614


host_id = {
                "jsonrpc": "2.0",
                "method": "host.get",
                "params": {
                  "output": ["hostid", "host"],
                  "selectInterfaces": ["interfaceid", "ip"]},
                "id": 1,
                "auth": AUTHTOKEN
         }


host_status = {
                  "jsonrpc": "2.0",
                  "method": "host.get",
                  "params": {
                    "filter": {
                      "host": [
                        HOST_1,
                        HOST_2,
                        HOST_3]}},
                  "id": 1,
                  "auth": AUTHTOKEN
                }

host_group = {
                  "jsonrpc": "2.0",
                  "method": "hostgroup.get",
                  "params": {
                      "output": "extend",
                      "filter": {
                          "name": HOST_GROUP_NAME}},
                  "id": 1,
                  "auth": AUTHTOKEN
             }
logout = {
                  "jsonrpc": "2.0",
                  "method": "user.logout",
                  "params": {},
                  "id": 1,
                  "auth": AUTHTOKEN
               }
