#!/usr/bin/python3
import os
import yaml

def load_info(rundle):
    """
    Read the data from the rundle stored.  Return as a dictionary
    """
    plist = {}
    for name in os.listdir(rundle):
        if name.endswith('yaml'):
            pname = name.split('.')[0]
            fname = os.path.join(rundle,name)
            with open(fname, 'r') as fdesc:
                plist[pname] = yaml.safe_load(fdesc)
    return plist

if __name__ == "__main__":
    #
    # Use O'Brien's Pub as a guinea pig
    #
    plist = load_info("OBriensIrishPub")
    for entry in plist.keys():
        print(entry)
        print(plist[entry])
