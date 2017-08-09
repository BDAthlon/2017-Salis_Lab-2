# Circuit Globs

Circuit Globs aims to be a simple Python module to display the characteristic curves of simple genetic circuits. The aim is to define a set of genetic parts and reporter proteins that interact each other via a set of actions to maximize co-incidence of the curve produced with randomly populated green globs on a Xy plane. It is envisoned both as a game and a learning tool.

# Getting Started

Circuit Globs was developed in Python 2.7 and uses the standard Python science stack. You'll need `Numpy`, `Scipy` and `Matplotlib` and you are good to go! We recommend installation of [Anaconda](https://www.continuum.io/) on your system that ships with the latest versions of these packages.

# Module Structure

Circuit Globs comes with it's own original grammar for specifying programs for genetic circuits and a parser to translate those programs into intermediate data structures. These intermediate structures that are then used to derive ODEs for the genetic parts on the fly and capture their interplay. These ODEs are then solved to define the characteristics of the genetic circuits. `Matplotlib` is used to display randomly initialized green blobs (a manner of puzzle) and the ODE solutions are then plotted against them to determine the success of the system in matching the blobs.

* `gcparser.py` contains all functions to translate user-defined genetic circuit programs into data structures for ODE solver
* `model.py` contains all functions for deriving and solving the ODEs from the parsed circuit information
* `animate.py` contains all `Matplotlib` functions for initializing the random green blobs and animating the ODE solution
* `utils.py` is a placeholder module that housed tertiary functions that were eventually absorbed into the other three modules

# The Grammar

Circuit Globs programs are written in two major steps. At first the parts and reporter proteins are defined in a variable `species` as a Python multi-line comment. Each line in the species defines a single part of the circuit in the form `<part_name> <maximum_translation_rate> <initial_concentration>`. For example:

```
species = '''
    R1 60 10
    R2 60 50
    R3 60 10
    GFP 120 0
'''
```

