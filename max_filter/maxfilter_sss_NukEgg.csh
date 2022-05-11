#!/bin/tcsh
foreach i ( *raw{,-?}.fif )
  echo $i
  set n = `basename $i .fif`
  sudo /neuro/bin/util/maxfilter -gui -f $i -o ${n}_sss.fif
end
