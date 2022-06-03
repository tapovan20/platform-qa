##
## =============================================================================================
## IBM Confidential
## © Copyright IBM Corp. 2022
## The source code for this program is not published or otherwise divested of its trade secrets,
## irrespective of what has been deposited with the U.S. Copyright Office.
## =============================================================================================
##

#Configuration file
CONFIG_JSON=$HOME/zscpve/config.json
if [[ ! -s $CONFIG_JSON ]]; then
 echo "Error: Config file not found or zero length: $CONFIG_JSON" 1>&2
 exit 1
fi
#Rack and Sled ID.
Z_RACK=$(cat $CONFIG_JSON | jq -r '.ve.rack')
Z_SLED=$(cat $CONFIG_JSON | jq -r '.ve.sled')

#get Rack and Sled 
echo "Z_RACK: $Z_RACK";
echo "Z_SLED: $Z_SLED";

#Write these details to a file
echo "Z_RACK = $Z_RACK">> OUT.py
echo "Z_SLED = $Z_SLED">> OUT.py
echo "HOST_1 = 'r${Z_RACK}s${Z_SLED}stg0'">> OUT.py
echo "HOST_2 = 'r${Z_RACK}s${Z_SLED}stg1'">> OUT.py
echo "HOST_3 = 'r${Z_RACK}s${Z_SLED}stg2'">> OUT.py

#Read Storage node from the Node yaml file
Nodes_config=$HOME/.r${Z_RACK}s${Z_SLED}-vaultdir/r${Z_RACK}s${Z_SLED}.yml
STORAGE_NODES=`cat ${Nodes_config} | yq '.compute_node[] | select(.hostname | contains("stg"))' | jq -s -c 'sort_by(.hostname) | .[]'`
STORAGE_VE=`echo $STORAGE_NODES | jq -r '.hostIP' | awk '{print $1;}' | xargs`

#Convert the string to a space based array first
IFS=' ' read -r -a STORAGE_ARRAY <<< "${STORAGE_VE}"
echo "MASTER_IP = '${STORAGE_ARRAY[0]}'" >> OUT.py
echo "HOST_2_IP = '${STORAGE_ARRAY[1]}'" >> OUT.py
echo "HOST_3_IP = '${STORAGE_ARRAY[2]}'" >> OUT.py

echo "============================== Listing out your Storage Node IPs =============================="
echo "${STORAGE_ARRAY[@]}"




echo "===============Listing out the name of the hostname =========================================="
echo "Storage_hostname_1 is r${Z_RACK}s${Z_SLED}stg0"
echo "Storage_hostname_2 is r${Z_RACK}s${Z_SLED}stg1"
echo "Storage_hostname_3 is r${Z_RACK}s${Z_SLED}stg2"

#copying files to Master storage node where Zabbix server is running

scp -r $HOME/platform-qa/Zabbix_platform/Zabbix_smoke_test/zabbix_testing.py root@${STORAGE_ARRAY[0]}:/tmp > /dev/null
scp -r $HOME/platform-qa/Zabbix_platform/Zabbix_smoke_test/OUT.py root@${STORAGE_ARRAY[0]}:/tmp > /dev/null
scp -r $HOME/platform-qa/Zabbix_platform/Zabbix_smoke_test/generate_token.py root@${STORAGE_ARRAY[0]}:/tmp > /dev/null

#Running scripts on the node
echo  "In Master storage node ${STORAGE_ARRAY[0]}"
ssh root@${STORAGE_ARRAY[0]} 'python3 /tmp/generate_token.py'
scp -r $HOME/platform-qa/Zabbix_platform/Zabbix_smoke_test/payload.py root@${STORAGE_ARRAY[0]}:/tmp > /dev/null
sleep 2
ssh root@${STORAGE_ARRAY[0]} 'python3 /tmp/zabbix_testing.py'
sleep 2
scp -r root@${STORAGE_ARRAY[0]}:/tmp/zabbix.log $HOME/platform-qa/Zabbix_platform/Zabbix_smoke_test/zabbix.logs
