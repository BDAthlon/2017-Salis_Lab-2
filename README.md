# Circuit Globs

Circuit Globs aims to be a simple Python module to display the characteristic curves of simple genetic circuits. The aim is to define a set of genetic parts and reporter proteins that interact each other via a set of actions to maximize co-incidence of the curve produced with randomly populated green globs on a Xy plane. It is envisoned both as a game and a learning tool.

# Getting Started

Circuit Globs was developed in Python 2.7 and uses the standard Python science stack. You'll need `Numpy`, `Scipy` and `Matplotlib` and you are good to go! We recommend installation of [Anaconda](https://www.continuum.io/) on your system that ships with the latest versions of these packages.

# Module Structure

Circuit Globs comes with it's own original grammar for specifying programs for genetic circuits and a parser to translate those programs into intermediate data structures. These intermediate structures that are then used to derive ODEs for the genetic parts on the fly and capture their interplay. These ODEs are then solved to define the characteristics of the genetic circuit. `Matplotlib` is used to display randomly initialized green blobs (a manner of puzzle) and the ODE solutions are then plotted against them to determine the success of the system in matching the blobs.

* `gcparser.py` contains all functions to translate user-defined genetic circuit programs into data structures for ODE solver
* `model.py` contains all functions for deriving and solving the ODEs from the parsed circuit information
* `animate.py` contains all `Matplotlib` functions for initializing the random green blobs and animating the ODE solution
* `utils.py` is a placeholder module that housed tertiary functions that were eventually absorbed into the other three modules

# The Grammar

Circuit Globs programs are written in two major steps. At first the parts and reporter proteins are defined in a variable `species` as a Python multi-line string. Each line in the species defines a single part of the circuit in the form `<part_name> <maximum_translation_rate> <initial_concentration>`. For example:
```
species = '''
    R1 60 10
    R2 60 50
    R3 60 10
    GFP 120 0
'''
```
Here, we have three proteins R1, R2, R3 and a reporter protein RFP. Next, the actual program defining the circuit logic is written in the form `<part_i> <action> <part_j> (context_value_1,context_value_2)` as a multi-line string, stored in the variable `program`. All `part_name` being used in the program must be defined in the `species` variable, or else the `gcparser` module raises an execption. The `action` defines the effect `part_i` has on `part_j` and can be one of `<activates, represses, inverts>` type. The `context_value_1` and `context_value_2` imply different meaning in the context of specified action. In case of activation and repression they are `kd` and `n` values, while in case of inversion they are `p` and `t` values. For example, consider the following repressilator `program` for the above defined `species`:
```
program = '''
    R1 represses R2 (0.7,2)
    R2 represses R3 (0.7,2)
    R3 represses R1 (0.7,2)
    R1 represses GFP (0.7,2)
'''
```

# Example: Python program to design and simulate a repressilator

Once cloned/downloaded it is very easy to run Circuit Globs. Let's try to cover as many randomly generated green globs using the repressilator being discussed so far. Note: This example is present in and can be run from the examples directory along with a few more. Let's set up the basics.
```
# Make sure Python finds circuitsglobs modules
import numpy as np
import gcparser
import model
from animate import Puzzle, Graphics

# Makes the Puzzle consistent, can be changed or removed
import random
random.seed(12)
```
Now, that we have all modules we need, let's create a medium difficulty puzzle to solve (higher difficulty implies lesser globs most of which vary in sizes and scale down in diameter). We can even plot it and see before we attempt anything.
```
Puzzle1 = Puzzle(difficulty=6)
# Puzzle1.plot() # When uncommented displays the puzzle before solution
```
After we define the `species` and `program` as shown in The Grammar section, we create parsed structures:
```
def_struct, prg_struct = gcparser.get_parsed_struct(species, program)
```
Next, we create an instance of our ODE solver and solve the circuit ODEs.
```
odesolver = model.CircuitModel(def_struct, prg_struct)
(time, reporters, data) = odesolver.run()
```
Everything is done quickly...time to visualize our solution!
```
GraphicsObject = Graphics(time, data, Puzzle1.globs)
GraphicsObject.generate()
```
![repressilator.png](https://github.com/BDAthlon/2017-Salis_Lab-2/blob/master/repressilator.png "Circuit Glob: Repressilator")
