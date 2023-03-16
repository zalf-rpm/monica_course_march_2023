import json
import os
import csv

basepath = os.path.dirname(os.path.abspath(__file__))

files = [f for f in os.listdir(basepath) if os.path.isfile(os.path.join(basepath, f))]

for f in files:
    if "sim" not in f or ".json" not in f:
        continue
    
    print("reading " + f)
    with open(os.path.join(basepath, f)) as _:
        sim = json.load(_)
    
    sim["climate.csv"] = ""
    sim["include-file-base-path"] = "${MONICA_PARAMETERS}/..//"
    sim["output"]["events"] = []

    sim["output"]["csv-options"] = {}
    sim["output"]["csv-options"]["include-header-row"] = True
    sim["output"]["csv-options"]["include-units-row"] = True
    sim["output"]["csv-options"]["csv-separator"] = ","
    

    with open(os.path.join(basepath, f), "w") as out_f:
        json.dump(sim, out_f, indent=4)
        

print "done"


