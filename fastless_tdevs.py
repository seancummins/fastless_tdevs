#!/usr/bin/env python -u
# -*- coding: utf-8 -*-
"""
fastless_tdevs.py - Reports Symmetrix TDEVs that are in Storage Groups, but not managed by FASTVP

Requirements:
- Python 2.7.x (haven't tested in 3.x, but it might work)
- EMC Solutions Enabler
- SYMCLI bin directory in PATH

"""

import argparse
import subprocess
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


def symcli_gentree(command):
    command += ' -output xml_e'
    result = ET.fromstring(subprocess.check_output(command, shell=True))
    return result


### Define and Parse CLI arguments
parser = argparse.ArgumentParser(description='Reports Symmetrix TDEVs that are not managed by FASTVP.')
parser.add_argument('-sid', required=True, help='Symmetrix serial number')
args = parser.parse_args()

### Capture SG information into ET Tree
sgtree = symcli_gentree('symsg -sid %s list -v' % args.sid)

fastTdevs = set()   # FAST-managed TDEVs
allTdevs = set()    # All TDEVs (that are in SGs)

# Iterate through all Storage Groups, capturing membership info
for sg in sgtree.iterfind('SG'):
    for member in sg.iterfind('DEVS_List/Device'):
        dev_name = member.find('dev_name').text
        allTdevs.update([dev_name])
        if sg.find('SG_Info/FAST_Policy').text == "Yes":
            fastTdevs.update([dev_name])

print(", ".join(sorted(fastTdevs.symmetric_difference(allTdevs))))