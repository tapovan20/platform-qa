#
# =============================================================================================
# IBM Confidential
# © Copyright IBM Corp. 2022
# The source code for this program is not published or otherwise divested of its trade secrets,
# irrespective of what has been deposited with the U.S. Copyright Office.
# =============================================================================================
#

"""
This module will be used to read the environment and based on that run command.
"""
import subprocess
import sys
from conftest import confg # pylint: disable=E0401

class CephRun(object): # pylint: disable=R0205
    '''
    This class is used to read the environment and based on that run command
    '''

    @staticmethod
    def get_subprocess_cmd(command):
        '''
        This function is used to get the environment.
        '''
        env_dict=confg.get_env()
        try:
            if env_dict["environment"]=="MZONE":
                subprocess_command="gt -o raw -t 300 "+env_dict['storage_ip']+" "+command
            elif env_dict["environment"]=="VE":
                subprocess_command="ssh sysop@"+env_dict['storage_ip']+" "+command
            else:
                raise Exception
        except Exception:
            print("Please Provide the correct environment VE or MZONE")
            sys.exit(1)
        return subprocess_command
    def run_command(self,command):
        '''
        This function is used to run command
        '''
        subprocess_command=self.get_subprocess_cmd(command)
        with subprocess.Popen([subprocess_command],
                    stdin =subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True,
                    shell=True,
                    bufsize=0) as ssh:
            #Fetch output
            output, err = ssh.communicate()
            return output,err
