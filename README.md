# AccessControl-AcuteCare-Protocol
Code for experiments simulation used in paper "AC-AC: Dynamic Revocable Access Control for Acute Care Teams to Access Medical Records"

To run the experiments, follow the steps

1 - Install dependencies for Python3

2 - Populate database, constants can be changed in fill_users.py
- python3 manage.py shell < fill_users.py
 
3 - Run some experimental script
- python3 manage.py shell < experimental_scripts/SCRIPT_NAME.py

Note: Inside each script there's already an user | patient defined, this may be required to change or created.
