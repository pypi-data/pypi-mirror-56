#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test runman
"""

import runman
import cloudpickle as pickle
import os


def test_runman():
    """Test run management"""
    counter = []

    def step(timestep):
        counter.append(timestep)

    def log():
        if len(counter) == 0:
            logval = None
        else:
            logval = counter[-1]
        print(logval)
        return logval

    a_run = runman.Run(
        assets=[counter],
        stepfns=[step],
        logfns=[log],
        loginterval=2,
        snapshotinterval=4,
        serializewhat=["log", "timestep"],
    )
    a_run.run(10, True)
    filename = str(abs(hash(a_run))) + ".pkl"
    with open(filename, "rb") as file:
        reloaded = pickle.load(file)
    assert reloaded["timestep"] == a_run.timestep
    os.remove(filename)
