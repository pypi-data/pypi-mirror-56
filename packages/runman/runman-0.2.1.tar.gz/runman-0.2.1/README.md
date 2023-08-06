# Run Manager

[![Build Status](https://github.com/AllenCellModeling/runman/workflows/Build%20Master/badge.svg)](https://github.com/AllenCellModeling/runman/actions)
[![Documentation](https://github.com/AllenCellModeling/runman/workflows/Documentation/badge.svg)](https://AllenCellModeling.github.io/runman)

Mange runs (mostly of stochastic simulations)

---

## Features
* Register a world, functions to be called on each timestep, and functions that perform logging

## Quick Start
```python
import runman

counter = []
def step(timestep):
    counter.append(timestep)
def log():
    print(counter[-1])
    return counter[-1]

run = runman.Run(assets=[counter, ], 
                 stepfns=[step, ],
                 logfns=[log, ], 
                 loginterval=2)
run.run(10)
```

## Installation

Clone and install or `pip install git+https://github.com/AllenCellModeling/runman.git`

## Documentation
For full package documentation please visit [AllenCellModeling.github.io/runman](https://AllenCellModeling.github.io/runman).


Available under the Allen Institute Software License

