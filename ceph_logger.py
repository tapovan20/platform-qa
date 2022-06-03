#
# =============================================================================================
# IBM Confidential
# © Copyright IBM Corp. 2022
# The source code for this program is not published or otherwise divested of its trade secrets,
# irrespective of what has been deposited with the U.S. Copyright Office.
# =============================================================================================
#

''' Importing all the required funtions'''
import logging
import sys
import os


def get_logger(name):
    '''This function is used for logger information '''
    if not os.path.exists("ceph_smoke_logfiles"):
        os.makedirs("ceph_smoke_logfiles")
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    # filehandling
    handler = logging.FileHandler(f"ceph_smoke_logfiles/{name}.log", mode="w+")
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    # console_handler
    handler2 = logging.StreamHandler(sys.stdout)
    handler2.setLevel(logging.DEBUG)
    logger.addHandler(handler2)

    # this is calling a funtion
    frtm = logging.Formatter('%(asctime)s  %(name)s \
            %(levelname)s: %(message)s')

    # setting the handler
    handler.setFormatter(frtm)
    handler2.setFormatter(frtm)

    return logger
