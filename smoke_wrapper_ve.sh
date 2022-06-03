##
## =============================================================================================
## IBM Confidential
## © Copyright IBM Corp. 2022
## The source code for this program is not published or otherwise divested of its trade secrets,
## irrespective of what has been deposited with the U.S. Copyright Office.
## =============================================================================================
##

#Location of current script.
W_HERE=$(dirname $(readlink -f ${0}));
#Creating Log directory and removing previous run log directory
rm -rf VDEVLOGS
mkdir VDEVLOGS 2>/dev/null
#copying expected output for ve
cp tests/expected_output_ve.py tests/expected_output.py
#Configuration file
CONFIG_JSON=$HOME/zscpve/config.json
if [[ ! -s $CONFIG_JSON ]]; then
 echo "Error: Config file not found or zero length: $CONFIG_JSON" 1>&2
 exit 1
fi
#Rack and Sled ID.
Z_RACK=$(cat $CONFIG_JSON | jq -r '.ve.rack')
Z_SLED=$(cat $CONFIG_JSON | jq -r '.ve.sled')
echo "Z_RACK: $Z_RACK";
echo "Z_SLED: $Z_SLED";
#Read Storage node from the Node yaml file
Nodes_config=$HOME/zscpve/build/Hephaestus/cfg/platform-inventory/region/virtual/dal13g4/netboot100/config/r${Z_RACK}s${Z_SLED}_acadia.yml
STORAGE_NODES=`cat ${Nodes_config} | yq '.compute_node[] | select(.hostname | contains("stg"))' | jq -s -c 'sort_by(.hostname) | .[]'`
STORAGE_VE=`echo $STORAGE_NODES | jq -r '.hostIP' | awk '{print $1;}' | xargs`
#Convert the string to a space based array first
IFS=' ' read -r -a STORAGE_ARRAY <<< "${STORAGE_VE}"
echo "============================== Listing out your Storage Node IPs =============================="
echo "${STORAGE_ARRAY[@]}"
declare -i y=0
for i in "${STORAGE_ARRAY[@]}"
do
 declare -i zero=0
 if [[ $y -eq $zero ]]
 then
 eval IP=${i}
 echo "============================== Running Smoke Tests on your Master Storage Node $IP =============================="
 echo "=============================== Capturing OS version of the storage node ========================================"
 date >> os_version.txt
 echo " On Node" $IP >> os_version.txt
 lsb_release -d >> os_version.txt
#Installing the Python Requirements in VDEV
 python3 -m pip install -r requirements.txt --user > /dev/null

#Running Smoke and encryption test on Master node and copying logs to VDEVLOG folder.
 python3 -m pytest test_smoke_runner.py -m smoke -s --html=ceph_smoke_logfiles/htmlreports/CEPH_smoke_report.html --env="VE" --storage_ip=$IP --capture=tee-sys
 scp -r $W_HERE/ceph_smoke_logfiles $W_HERE/VDEVLOGS/stg$y > /dev/null
 scp $W_HERE/ceph_smoke_logfiles/tests.CEPH_TESTING_FEATURES.ceph_encryption.log $W_HERE/VDEVLOGS/stg$y > /dev/null
 scp $W_HERE/ceph_smoke_logfiles/htmlreports/CEPH_encryption_report.html $W_HERE/VDEVLOGS/stg$y/htmlreports > /dev/null
 else
 eval IP=${i}
 echo "============================== Running Smoke Tests on your Storage Node $IP =============================="
 echo
 echo "=============================== Capturing OS version of the storage node ========================================"
 date >> os_version.txt
 echo " On Node" $IP >> os_version.txt
 lsb_release -d >> os_version.txt
#Running smoke test on remaining stg nodes
 python3 -m pytest test_smoke_runner.py -m encryption -s --html=ceph_smoke_logfiles/htmlreports/CEPH_encryption_report.html --env="VE" --storage_ip=$IP --capture=tee-sys
 #Take the reports and copy it back to VE
 mkdir $W_HERE/VDEVLOGS/stg$y
 mkdir $W_HERE/VDEVLOGS/stg$y/htmlreports
 scp $W_HERE/ceph_smoke_logfiles/tests.CEPH_TESTING_FEATURES.ceph_encryption.log $W_HERE/VDEVLOGS/stg$y > /dev/null
 scp $W_HERE/ceph_smoke_logfiles/htmlreports/CEPH_encryption_report.html $W_HERE/VDEVLOGS/stg$y/htmlreports > /dev/null 
 fi
 y=$((y+1))
done

