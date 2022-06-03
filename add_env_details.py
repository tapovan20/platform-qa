#
# =============================================================================================
# IBM Confidential
# © Copyright IBM Corp. 2022
# The source code for this program is not published or otherwise divested of its trade secrets,
# irrespective of what has been deposited with the U.S. Copyright Office.
# =============================================================================================
#

import yaml
import json

with open("deploy_ver.yaml") as stream:
    deploy_ver_obj = (yaml.safe_load(stream))

with open("op.json",'w+') as jo:
    json.dump(deploy_ver_obj,jo)

with open("op.json") as data1:
    deploy_version_list = json.load(data1)
    with open(".report.json",'r+') as file:
        data = json.load(file)  # get data from file
        data.update(deploy_version_list[0])
        file.seek(0)
        x = json.dump(data, file,indent=4)  # insert data in file

with open("release_bundles") as stream1:
    release_bundle_list = stream1.read().splitlines()
    print(release_bundle_list)
    for line in release_bundle_list:
        if ":" in line:
            x =line.split(":")
            with open(".report.json",'r+') as file1:
                data = json.load(file1)
                data[x[0]]=x[1]+x[2]+x[3]
                file1.seek(0)
                json.dump(data,file1,indent =4)
