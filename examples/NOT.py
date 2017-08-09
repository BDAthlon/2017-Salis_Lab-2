# Tackling a difficult Circuit-Glob puzzle with the repressilator

import sys
sys.path.append('../circuitglobs')

import numpy as np
import gcparser
import model
from animate import Puzzle, Graphics

import random
random.seed(320)

if __name__ == "__main__":

    Puzzle1 = Puzzle(difficulty=2)
    # Puzzle1.plot()

    '''
    Circuit Globs Grammar
    Species: Statements of the form <var> <max_trans_rate> <init_conc>
    Program: Statements of the form <var_i> <action> <var_j> <(val_1, val_2)>
    Actions: Operations from <represses, activates, inverts>
    '''

    species = '''
    R 0.5 0
    GFP 75 0
    '''

    program = '''
    R represses GFP (1.1,1.5)
    '''
    a, b = gcparser.get_parsed_struct(species, program)

    odesolver = model.CircuitModel(a,b)
    (time,reporters,data) = odesolver.run()

    GraphicsObject = Graphics(time,data,Puzzle1.globs)
    GraphicsObject.generate()
