#!/bin/bash
##
## =============================================================================================
## IBM Confidential
## © Copyright IBM Corp. 2022
## The source code for this program is not published or otherwise divested of its trade secrets,
## irrespective of what has been deposited with the U.S. Copyright Office.
## =============================================================================================
##


rm -f bin/qa-containers.tgz

save_containers='genctl-acadia/platform-qa-robot:latest genctl-acadia/platform-qa-performance:latest'

echo "Saving containers:"
for i in ${save_containers};
do
    echo "  - ${i}"
done

mkdir -p bin
docker image save ${save_containers} | gzip -c > bin/qa-containers.tgz
exit $?
