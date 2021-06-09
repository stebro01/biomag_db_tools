
#!/bin/tcsh
foreach i ( *raw{,-?}.fif )
  echo $i
  set n = `basename $i .fif`
  sudo /neuro/bin/util/maxfilter -gui -f $i -o ${n}_sss_trans.fif -trans /BIOMAG_DATA/STORAGE/template_MAXFILTER/Virginie_MID_1_avg.fif
end

