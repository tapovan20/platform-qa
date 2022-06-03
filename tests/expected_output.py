#
# =============================================================================================
# IBM Confidential
# © Copyright IBM Corp. 2022
# The source code for this program is not published or otherwise divested of its trade secrets,
# irrespective of what has been deposited with the U.S. Copyright Office.
# =============================================================================================
#

'''
This module contains the expected output.
'''
#from globals import ENV
import names

#CEPH VERSION
VERSION_ID = "16.2.0-117.el8cp"
VERSION_STATE = "(stable)"

#CEPH HEALTH
HEALTHOK = 'HEALTH_OK'
HEALTHWARN = 'HEALTH_WARN'

#CEPH POOLS
POOLS = ["device_health_metrics", "libvirt-pool"]

#CEPH DEVICE CLASS
#if ENV=='MZONE':
# DEVICE_CLASS = ["ssd"]
#else:
DEVICE_CLASS = ["hdd"]

#OSD TREE STATUS AND REWEIGHT
UP = 'up'
REWEIGHT_VALUE = 1.0

#PG STATS
PG_STATUS='active+clean'

#MON STATS
MAX_MONS = 3

#CLUSTER UTILIZATION DF
MAX_UTILIZATION = 75

#RBD IMAGE NAME
name = names.get_first_name()
RBD_IMAGE_NAME = name

#RBD POOL NAME
RBD_POOL_NAME= "libvirt-pool"

#CEPH IMAGE SIZES
MAX_IMAGE_SIZE = 2147483648
MIN_IMAGE_SIZE = 1073741824

#RBD SNAPSHOT NAME
RBD_SNAPSHOT_NAME = "snap"

#ceph_mgr
Expected_modules=[ "balancer",
        "crash",
        "devicehealth",
        "orchestrator",
        "pg_autoscaler",
        "progress",
        "rbd_support",
        "status",
        "telemetry",
        "volumes"
    ]
Enabled_modules = [
        "acadia",
        "cephadm",
        "iostat",
        "restful",
        "zabbix"
]
capabilities={'mds': 'allow *', 'mon': 'profile mgr', 'osd': 'allow *'}

# Containerised services
CONTAINERISED_SERVICES_LIST=["acadia_key_provider","acadia_cluster_registration","node_exporter"]
