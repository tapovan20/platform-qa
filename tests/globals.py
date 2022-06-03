#
# =============================================================================================
# IBM Confidential
# © Copyright IBM Corp. 2022
# The source code for this program is not published or otherwise divested of its trade secrets,
# irrespective of what has been deposited with the U.S. Copyright Office.
# =============================================================================================
#

"""
This module contains the global variables used by smoke test.
"""

SLEEP_CONSTANT = 3

#STATUS KEYS
HEALTH = 'health'
STATUS = 'status'
OSDMAP = 'osdmap'
NUM_OSDS = 'num_osds'
NUM_UP_OSDS = 'num_up_osds'
NUM_IN_OSDS = 'num_in_osds'

#OSD POOLS
POOLNAME = 'poolname'

#OSD TREE KEYS
NODES = 'nodes'
CHILDREN = 'children'
POOLWEIGHT = 'pool_weights'
REWEIGHT = 'reweight'

#PG STATS KEYS
PG_SUMMARY = 'pg_summary'
NUM_PG_BY_STATE = 'num_pg_by_state'
NAME = 'name'
ID = 'id'

#CEPH MON STATS KEY
NUM_MONS = 'num_mons'
EPOCH = 'epoch'

#Ports
Ports = "3300 6800"

#CEPH DF KEYS
STATS_BY_CLASS = 'stats_by_class'
TOTAL_USED_RAW_RATIO = 'total_used_raw_ratio'

#CEPH OSD DF KEYS
UTILIZATION = 'utilization'

#CEPH IMAGE SIZES
SIZE = 'size'
