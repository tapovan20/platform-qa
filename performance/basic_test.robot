*** Settings ***
Library    OperatingSystem
Task Setup    Set Environment Variable    CEPH_ARGS    -c /host/var/lib/acadia/qa/ceph.conf -n client.qa-client --keyring /host/var/lib/acadia/qa/ceph.client.qa-client.keyring

*** Variables ***
${acadia_pool_name}=  libvirt-pool

*** Test Cases ***
Basic Test
    ${output}=  Run  rados bench -p ${acadia_pool_name} 10 write
    Log  ${output}  console=yes