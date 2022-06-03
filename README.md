# acadia-platform-test
##### Platform Test Automation Suite

### Setup
- ssh dal13g4-vdev1 (Vdev) or ssh deployer (Mzone)
- Clone the repository - `git@github.ibm.com:genctl-acadia/platform-qa.git`

### Steps to run the test
- cd to `smoke_test/`
- Start the test by running the shell script 
   - For Vdev, run 
   `./smoke_wrapper_ve.sh`
   - For Mzone, run 
   `./smoke_wrapper_mzone.sh /home/tsharma/repos/platform-inventory/region/mzone1234.yml smoke encryption`
      - :warning: Set the context before running the script on Mzone `gt -Z mzone1234`

### Note
The script will auto-install all requirements (locally for root user) and will run the smoke test from the deployer for the specified environment (VE/Mzone).
- Run selective test cases by giving the pytest marker fixtures in the shell script
   - `smoke` - Runs a smoke test for all the test cases
   - `health` - Runs Ceph health check related tests
   - `pool`  - Runs Ceph Pools, PGs and OSDs tests
   - `keyring`- Runs Ceph authentication and keyring tests
   - `rbd`  - Runs Ceph RBD tests 
   - `encryption` - Runs Ceph encryption at rest tests
- Logs and reports will be generated in `VDEVLOGS` folder at the end of the run for VE.
- Logs and reports will be generated in `MZONELOGS` folder at the end of the run for Mzone.

### Steps to add new test
Refer https://confluence.swg.usma.ibm.com:8445/pages/viewpage.action?pageId=240390494
