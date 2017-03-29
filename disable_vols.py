import json
import os
import subprocess


p = subprocess.check_output(['yinst','ssh', '-h', 'sm-pool101.flickr.bf2.yahoo.com', '/home/jukim/find-oversized-vols.sh'])
print p


def close_volumes(original, vols):
    x = original
    formatted = open('formatted_file.json', 'w')

    with open(x, 'r') as f:
         raw_data = "{\n"  + f.read() + "\n}"
         data = json.loads(raw_data)

    for volume in vols:
         data[volume]['allow_new'] = 0

    data = json.dumps(data, indent=4, sort_keys=True)

    formatted.write(data)
    formatted.close()


with open('oversized-vols.txt') as f:
    content = f.read().splitlines()

# walk through volume list
close_volumes("farm9.vols-practice.json", content)
