import json
import os
import csv

basepath = os.path.dirname(os.path.abspath(__file__))

files = [f for f in os.listdir(basepath) if os.path.isfile(os.path.join(basepath, f))]

for f in files:
    if "site" not in f or ".json" not in f:
        continue
    
    print("reading " + f)
    with open(os.path.join(basepath, f)) as _:
        lines = _.readlines()
    
    towrite = []
    for l in lines:
        if "monica_simulation_setup/" in l:
            l = l.replace("monica_simulation_setup/", "")
        if "monica_parameters/" in l:
            l = l.replace("monica_parameters/", "monica-parameters/")
       
        #print l
        towrite.append(l)
    
    with open(os.path.join(basepath, f), "w") as out_f:
        for line in towrite:
            out_f.write(line)

print "done"


