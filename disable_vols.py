import json
import os
import subprocess
import sys

# login to remote sm-pool host and retrieve list of oversized vols
p = subprocess.check_output(['yinst','ssh', '-h', 'sm-pool101.flickr.bf2.yahoo.com', '/home/jukim/find-oversized-vols.sh'])

try:
    p = subprocess.check_output(['yinst','ssh', '-h', 'sm-pool101.flickr.bf2.yahoo.com', '/home/jukim/find-oversized-vols.sh'],stderr= subprocess.STDOUT)
    print "I'm here: %s" % (p)
except subprocess.CalledProcessError as e:
    print "Error occured: %s" % (e)

# save the list of oversized vols onto a file on the localhost
f = open('sm-pool101_bf2_oversized_vols.txt', 'w')
f.write(p)
f.close()

# main function begins here
def close_volumes(original, vols):
    formatted = open('formatted_file.json', 'w')
    
    # original file is not a standard JSON, so have to add opening and ending curly brace
    with open(original, 'r') as f:
         raw_data = "{\n"  + f.read() + "\n}"
         formatted_data = json.loads(raw_data)

    # actually iterates through the oversized vols and changes the key-value is the oversized vol exists in the JSON    
    for volume in vols:
         try:
             formatted_data[volume]['allow_new']
         except KeyError:
             print "Key doesn't exist in this .json file so skipping..."
             continue
         formatted_data[volume]['allow_new'] = 0

    # format back to JSON
    final_data = json.dumps(formatted_data, indent=4, sort_keys=True)

    formatted.write(final_data)
    formatted.close()

with open('sm-pool101_bf2_oversized_vols.txt') as f:
    content = f.read().splitlines()

# give user the option to choose which original JSON file to edit
filename = sys.argv[1]
close_volumes(filename, content)
