#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cloudpickle as pickle


class Run:
    def __init__(
        self,
        assets=[],
        stepfns=[],
        logfns=[],
        loginterval=None,
        snapshotinterval=None,
        serializewhat="log",
    ):
        """Create a run to track changes sets of objects

        Parameters
        ----------
        assets: list
            Things we care about for this run stored to be serialized
        stepfns: list
            Set of functions to be called each timestep with signature
            fn(timestep)
        logfns: list
            Set of functions to be called each log interval and whose
            output is recorded
        loginterval: int or None
            How many timesteps between logging events, None disables logging
        shapshotinterval: int or None
            How many timesteps between snapshots (for recovery)
        serializewhat: str or list of strings
            What to serialize, inclusive of 'log', 'assets', 'timestamp',
            and 'run'
        """
        self.assets = list(assets)
        self.stepfns = list(stepfns)
        self.logfns = list(logfns)
        self.loginterval = loginterval
        self.snapshotinterval = snapshotinterval
        self.serializewhat = serializewhat
        self.timestep = 0
        self.log = []

    def step(self):
        """Move forward a single timestep"""
        for fn in self.stepfns:
            fn(self.timestep)
        self.timestep += 1

    def run(self, run_length, serialize=False):
        """Run for a time, optionally serializing at the end

        Parameters
        ----------
        run_length: int
            how many timesteps to run for
        serialize: bool
            whether or not to serialize the output at the end of the run
        """
        logint, snapint = self.loginterval, self.snapshotinterval
        for i in range(run_length):
            if logint is not None and self.timestep % logint == 0:
                self.log.append([fn() for fn in self.logfns])
            if snapint is not None and self.timestep % snapint == 0:
                self.serialize(what="run")
            self.step()
        if serialize:
            self.serialize()

    def serialize(self, fn=None, what=None):
        """Serialize the state of bits of the run to fn.

        Parameters
        ----------
        fn: str or None
            filename to save serialized run to
        what: str, list, or None
            what to serialize, possibilities are log, assets, timestep,
            and run. Defaults to the contents of self.serializewhat.
        """
        # deal with name
        if fn is None:
            fn = str(abs(self.__hash__())) + ".pkl"
        # create dict to serialize
        if what is None:
            what = self.serializewhat
        if type(what) is str:
            what = [
                what,
            ]
        assert all([k in ("log", "assets", "timestep", "run") for k in what])
        ser = {
            k: v
            for k, v in (
                ("log", self.log),
                ("assets", self.assets),
                ("timestep", self.timestep),
                ("run", self),
            )
            if k in what
        }
        # dump to file
        with open(fn, "wb") as file:
            pickle.dump(ser, file)
        return
