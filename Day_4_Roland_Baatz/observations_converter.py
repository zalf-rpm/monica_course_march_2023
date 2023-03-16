import os
import csv
from datetime import date, timedelta

def convertdate(datestring):
    day = int(datestring.split("/")[0])
    month = int(datestring.split("/")[1])
    year = int(datestring.split("/")[2])

    mydate = date(year, month, day)
    return mydate

def convert2row(exp, doy, stage, cv):
    row=[]
    row.append(exp)
    row.append(stage)
    row.append(doy)
    row.append(cv)

    return row


basepath = os.path.dirname(os.path.abspath(__file__))

raw_obs_file = basepath + "/cal2_phenology_mgt_soil_data.txt"
converted_obs_file = basepath +"/converted_obs.csv"

with open(converted_obs_file, "wb") as out_file:
    writer = csv.writer(out_file)
    header = ["exp_ID", "stage", "DOY", "cv"]
    writer.writerow(header)

    with open(raw_obs_file) as in_file:
        dialect = csv.Sniffer().sniff(in_file.read(), delimiters=';,\t')
        in_file.seek(0)
        reader = csv.reader(in_file, dialect)
        next(reader, None)  # skip the header
        for row in reader:
            exp = row[0]
            cv = row[99]
            BBCH30 = row[102]
            BBCH55 = row[103]
            if BBCH30 == "NA":
                continue

            date30 = convertdate(BBCH30)
            #datedr = date30 - timedelta(days=7)
            date55 = convertdate(BBCH55)
            #dateflo = date55 +timedelta(days=7)

            writer.writerow(convert2row(exp=exp, doy=date30.timetuple().tm_yday, stage="30", cv=cv))
            writer.writerow(convert2row(exp=exp, doy=date55.timetuple().tm_yday, stage="55", cv=cv))            

print "finished"