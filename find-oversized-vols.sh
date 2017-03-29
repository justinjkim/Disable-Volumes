#!/bin/bash

for i in $(/home/y/libexec/yms/flickr_yms_check_sm_volumes 2>&1 | grep full | awk '{print $2}'); do df -k /mnt/*/$i; done | grep photos | awk '{if ($3 < 629145600) print $3,$4,$5}' | cut -d '/' -f 4 | sort -n
