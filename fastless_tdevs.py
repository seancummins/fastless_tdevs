#!/usr/bin/env python -u
# -*- coding: utf-8 -*-
"""
fastless_tdevs.py - Reports Symmetrix TDEVs that are not managed by FASTVP
 
Requirements:
- Python 2.7.x (haven't tested in 3.x, but it might work)
- EMC Solutions Enabler
- SYMCLI bin directory in PATH
 
"""
 
import argparse
import subprocess
from lxml import etree
 
 
def symcli_gentree(command):
    command += ' -output xml_e'
    result = etree.fromstring(subprocess.check_output(command, shell=True))
    return result
 
 
### Define and Parse CLI arguments
parser = argparse.ArgumentParser(description='Shows TDEVs not managed by FASTVP.')
parser.add_argument('-sid', required=True, help='Symmetrix serial number')
args = parser.parse_args()
 
### Generate ElementTree objects from SYMCLI commands
sgET = symcli_gentree('symsg -sid %s list -v' % args.sid)
tdevET = symcli_gentree('symcfg -sid %s list -tdev -detail' % args.sid)
 
# Add all TDEVs from 'symcfg list' to tDevs set
# Modified to find only bound devices
tDevs = set(tdevET.xpath('.//ThinDevs/Device/pool[tdev_status="Bound"]/../dev_name/text()'))
 
# Add all TDEVs in FAST-Associated SGs to fDevs set
fDevs = set(sgET.xpath('.//SG_Info[FAST_Policy="Yes"]/../DEVS_List//dev_name/text()'))
 
# CSV-print the difference between tDevs and fDevs
print(', '.join(tDevs - fDevs))

