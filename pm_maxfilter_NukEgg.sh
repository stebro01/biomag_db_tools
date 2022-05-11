#!/bin/bash
# usage: just navigate to the folder containing your fif files, then: pm_maxfilter

pn=$(pwd)
cmd="cd ${pn} && ls -la && csh /BIOMAG_DATA/scripts/max_filter/maxfilter_sss_NukEgg.csh"
echo "execute: ${cmd}"
sshpass -p '123' -v ssh maxuser@ulm $cmd
