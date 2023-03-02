#!/usr/bin/python
# -*- coding: UTF-8

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/. */

# Authors:
# Michael Berg-Mohnicke <michael.berg@zalf.de>
#
# Maintainers:
# Currently maintained by the authors.
#
# This file has been created at the Institute of
# Landscape Systems Analysis at the ZALF.
# Copyright (C: Leibniz Centre for Agricultural Landscape Research (ZALF)

import csv
import json
import os
import sys
import zmq

def run_consumer(server = {"server": None, "port": None}):
    "collect data from workers"

    config = {
        "port": server["port"] if server["port"] else "7777",
        "server": server["server"] if server["server"] else "localhost", 
        "path_to_out_file": "out.csv"
    }
    if len(sys.argv) > 1 and __name__ == "__main__":
        for arg in sys.argv[1:]:
            k, v = arg.split("=", maxsplit=1)
            if k in config:
                config[k] = v.lower() == "true" if v.lower() in ["true", "false"] else v 
    print("config:", config)
    
    context = zmq.Context()
    socket = context.socket(zmq.PULL)

    socket.connect("tcp://" + config["server"] + ":" + config["port"])

    #socket.RCVTIMEO = 1000
    leave = False
    
    #envs = set()
    #for i in range(1, 1944):
    #    envs.add(i)

    def process_message(msg):

        if not hasattr(process_message, "received_env_count"):
            process_message.received_env_count = 0

        leave = False

        if msg["type"] == "finish":
            print("c: received finish message")
            leave = True

        else:
            print("c: received work result ", process_message.received_env_count, " customId: ", str(msg.get("customId", "")))
            
            process_message.received_env_count += 1

            if not os.path.exists(config["path_to_out_file"]):
                with open(config["path_to_out_file"], "w", newline="") as _:
                    writer = csv.writer(_, delimiter=",")
                    writer.writerow(["id", "sowing_doy", "kg N", "mm irrigation", "year", "sowing date", "harvest date", "yield", "AbBiom"])    

            #with open("out/out-" + str(i) + ".csv", 'wb') as _:
            with open(config["path_to_out_file"], "a", newline="") as _:
                writer = csv.writer(_, delimiter=",")

                cid = msg["customId"]
                #envs.remove(cid["env-id"])

                for data_ in msg.get("data", []):
                    results = data_.get("results", [])

                    #print("len(results)=", len(results))
                    for r in results:
                        if len(r) == 0:
                            continue
                        row = [cid["id"], cid["sowing_doy"], cid["nfert"], cid["irrigation"]]
                        row.append(r["harvest-year"])
                        row.append(r["sowing"])
                        row.append(r["harvest"])
                        row.append(r["Yield"])
                        row.append(r["AbBiom"])
                        writer.writerow(row)

        #print(envs)
        return leave

    while not leave:
        try:
            msg = json.loads(socket.recv_string(encoding="latin-1"))
            leave = process_message(msg)
        except:
            print(sys.exc_info())
            continue

    print("exiting run_consumer")

if __name__ == "__main__":
    run_consumer()
    