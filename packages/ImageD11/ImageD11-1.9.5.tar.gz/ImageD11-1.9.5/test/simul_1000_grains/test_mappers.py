
from __future__ import print_function
import sys, os

args = {
    'flt' : os.path.join("Al1000","Al1000.flt"),

    'par' : os.path.join("Al1000","Al1000.par"),
    'ubi' : "shaken.map"
    }

# 1: Run makemap.py
cmd1 = "python ../../scripts/makemap.py -f %(flt)s -p %(par)s -s cubic --omega_no_float --no_sort "%args
if 1:
    cmd2 = "-U allgrid_makemap.map -t 0.015 -u %(ubi)s"%args
    os.system(cmd1+cmd2)
    cmd2 = "-U allgrid_makemap.map -t 0.0075 -u allgrid_makemap.map"
    os.system(cmd1+cmd2)
if 1:
    cmd2 = "-U allgrid_makemap.map -t 0.0075 -u allgrid_makemap.map"
    os.system(cmd1+cmd2)
    


    

#args['flt']= os.path.join("ideal.flt")


if 1:
    # 2: Run sandbox/fittrans using assigned grains
    cmd = "python ../../sandbox/fittrans.py %(flt)s.new %(par)s %(ubi)s allgrid_fittrans.map "%args
    os.system( cmd)
    print( cmd)
if 1:
    # 3: Run ImageD11/indexer using assigned grains
    cmd = "python ../../ImageD11/indexer.py %(par)s %(flt)s.new fit %(ubi)s allgrid_indexer.map"%args
    os.system(cmd)
    print (cmd)
# 4: Run sandbox/teo.py  using assigned grains
if 1:
    cmd = "python ../../sandbox/teo.py %(flt)s.new %(par)s %(ubi)s allgrid_teo.map"%(args)
    os.system( cmd)


if  not os.path.exists("ideal.map"):
    os.system("python res2map.py Al1000/Al1000.ubi Al1000/Al1000.res ideal.map")

os.system("python compare.py")
