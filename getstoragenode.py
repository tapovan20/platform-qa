#
# =============================================================================================
# IBM Confidential
# © Copyright IBM Corp. 2022
# The source code for this program is not published or otherwise divested of its trade secrets,
# irrespective of what has been deposited with the U.S. Copyright Office.
# =============================================================================================
#

'''This script will be used to get the list of storage
node IPs and json output of storage node IPs
'''
import os
import json


def get_storage_node_ips():
    # pylint: disable-msg=too-many-locals
    ''' This function gets the storage node information '''
    # variables to get file path storage node path
    home_directory = os.path.expanduser("~")
    # get the working directory
    get_pwd = os.getcwd()
    # get file path
    file_path = home_directory+"/zscpve/build/iaasdeploy/rulerenv/ssh-config"
    storage_node_path = get_pwd+"/storagenode.json"
    # get the list of the storage node
    stg_node_list = []
    storage_node_ip_list = []
    with open(file_path, encoding="UTF-8") as fileobj:
        data = fileobj.read().split('\n')
        count = 0
        startcount = False
        key = ''
        for line in data:
            if (startcount is True)and(count < 4):
                count += 1
                stg_l = len(stg_node_list)-1
                line_s = line.split(" ")[3]
                stg_node_list[stg_l][key][line.split(" ")[2]] = line_s
                if count == 4:
                    startcount = False
                    count = 0
            elif "stg" in line and len(line.split(" ")) <= 3:
                stg_node_list.append({})
                stg_node_list[len(stg_node_list)-1][line.split(" ")[1]] = {}
                startcount = True
                key = line.split(" ")[1]
    with open(storage_node_path, 'w', encoding="UTF-8") as fileobj:
        json.dump(stg_node_list, fileobj)

    for st_node in stg_node_list:
        st_node_key = list(st_node.keys())[0]
        storage_node_ip_list.append(st_node[st_node_key]['Hostname'])
        sorted_list = sorted(storage_node_ip_list,
                             key=lambda x: int(x.rsplit('.', 1)[1]))
    return sorted_list


if __name__ == '__main__':
    get_node_ip = get_storage_node_ips()
    print(get_node_ip)
