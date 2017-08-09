# Tackling a difficult Circuit-Glob puzzle with the repressilator

import sys
sys.path.append('../circuitglobs')

import numpy as np
import gcparser
import model
from animate import Puzzle, Graphics

import random
random.seed(12)

if __name__ == "__main__":

    Puzzle1 = Puzzle(difficulty=6)
    # Puzzle1.plot()

    '''
    Circuit Globs Grammar
    Species: Statements of the form <var> <max_trans_rate> <init_conc>
    Program: Statements of the form <var_i> <action> <var_j> <(val_1, val_2)>
    Actions: Operations from <represses, activates, inverts>
    '''

    species = '''
    R1 60 10
    R2 60 50
    R3 60 10
    GFP 120 0
    '''

    program = '''
    R1 represses R2 (0.7,2)
    R2 represses R3 (0.7,2)
    R3 represses R1 (0.7,2)
    R1 represses GFP (0.7,2)
    '''
    a, b = gcparser.get_parsed_struct(species, program)

    odesolver = model.CircuitModel(a,b)
    (time,reporters,data) = odesolver.run()

    GraphicsObject = Graphics(time,data,Puzzle1.globs)
    GraphicsObject.generate()
