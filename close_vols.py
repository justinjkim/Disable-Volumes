#!/usr/bin/env python2.7
# This script creates a new .json file and automatically closes oversized vols resulting from the oversized-vols.sh script 
import json
import subprocess
import sys
import time

start_time = time.time()


# retrieves list of oversized vols from sm-pool101.flickr.bf2
try:
    p = subprocess.check_output(["/usr/bin/ssh", "-q", "-n", "sm-pool101.flickr.bf2.yahoo.com", "/home/y/tmp/find-oversized-vols.sh"], stderr=subprocess.STDOUT)
    print "I'm here:\n %s" % (p)
except subprocess.CalledProcessError as e:
    print "Error occured: %s" % (e)
f1 = open('sm-pool101_bf2_oversized_vols.txt', 'w')
f1.write(p)
f1.close()



def close_volumes(original, vols):
    #because the original .json files are not properly formatted .json files, we have to create a new file and make it into a real .json so that we can use the json module  """

    strip_comma = "sed -i '$s/},/}/' " + original
    subprocess.Popen([strip_comma], shell=True)

    formatted = open('formatted_file.json', 'w')
    with open(original, 'r') as f2:
        raw_data = "{\n" + f2.read() + "\n}"
        formatted_data = json.loads(raw_data)
    for volume in vols:
        try:
            formatted_data[volume]['allow_new'] = 0
            print "Volume %s: Setting allow_new to 0" % (volume)
        except KeyError:
            print "Volume %s doesn't exist in this particular .json...wrong farm?" % (volume)
            continue

    # write json when done
    final_data = json.dumps(formatted_data, indent=4, sort_keys=True)
    formatted.write(final_data)
    formatted.close()


filename = sys.argv[1]
with open('sm-pool101_bf2_oversized_vols.txt') as f3:
    content = f3.read().splitlines()

# actually call and run the script!
close_volumes(filename, content)

# take out the opening and ending curly brace
with open('formatted_file.json', 'r') as fin:
    data = fin.read().splitlines(True)
with open('formatted_file.json', 'w') as fout:
    fout.writelines(data[1:-1])



def reformat():
    reformat = "sed -e 's/^    //g' -e '$s/$/,/' -i formatted_file.json"
    try:
        subprocess.Popen([reformat], shell=True)
        print "Ok, deleted the whitespaces..."
    except:
        print "Hmm, something wrong in removing the white spaces..."

reformat()


print "This script took %s seconds to execute." % (time.time() - start_time)
