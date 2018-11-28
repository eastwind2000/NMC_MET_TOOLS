#!/usr/bin/env ipython

import os
import datetime, time


from ecmwfapi import ECMWFDataServer


d1 = datetime.datetime(2017, 06, 01, 00)

for i in range(365*8+180):

    cdate1 = d1.strftime("%Y-%m-%d")

    d2 = d1 + datetime.timedelta(hours=24)

    d1 = d2

    cdate2 = d2.strftime("%Y-%m-%d")

    print(cdate2)

    server = ECMWFDataServer()

    server.retrieve({
            "class": "ei",
            "dataset": "interim",
            "date": cdate2 + "/to/" + cdate2,
            "expver": "1",
            "grid": "0.75/0.75",
            "levtype": "sfc",
            "param": "142.128/143.128/228.128",
            "step": "12",
            "stream": "oper",
            "time": "00:00:00/12:00:00",
            "type": "fc",
            "format": "netcdf",
            "target": "ec_interim_tp_"+cdate2+".nc",
        })


