#!/usr/bin/python
# -*- coding: utf-8 -*-
## Programming project for Secure Programming course at TUNI
##
## Key View - SEEC
## Utility to handle key lists
## 1. May. 2024

import yaml

def print_keys(key_list):
    """
    Pretty prints key lists
    """
    keys = yaml.safe_load(key_list)
    for key in keys:
        print("")
        uid = str(key['uids']).strip("[']")
        print(f"        UID: {uid}\n"+
              f"       Type: {key['type']}\n"+
              f"       Algo: {key['algo']}\n"+
              f"     Length: {key['length']}\n"+
              f"Fingerprint: {key['fingerprint']}\n"
        )
    input("Press ENTER to quit\n")

def address_in_keys(addr, key_list) -> bool:
    """
    Finds if addr is in key_list
    """
    keys = yaml.safe_load(key_list)
    for key in keys:
        uid = str(key['uids']).strip("[']").split()
        address = uid[-1].strip('<>')
        if address == addr:
            return True
    return False
