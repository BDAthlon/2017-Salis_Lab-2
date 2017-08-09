# Tackling a difficult Circuit-Glob puzzle with the repressilator

import sys
sys.path.append('../circuitglobs')

import numpy as np
import gcparser
import model
from animate import Puzzle, Graphics

import random
random.seed(49)

if __name__ == "__main__":

    Puzzle1 = Puzzle(difficulty=4)
    # Puzzle1.plot()

    '''
    Circuit Globs Grammar
    Species: Statements of the form <var> <max_trans_rate> <init_conc>
    Program: Statements of the form <var_i> <action> <var_j> <(val_1, val_2)>
    Actions: Operations from <represses, activates, inverts>
    '''

    species = '''
    A 1 5
    I  100 1
    GFP 0.75 0
    '''

    program = '''
    A activates GFP (0.8,1)
    I inverts GFP (1,10)
    '''
    a, b = gcparser.get_parsed_struct(species, program)

    odesolver = model.CircuitModel(a,b)
    (time,reporters,data) = odesolver.run()
    
    GraphicsObject = Graphics(time,data,Puzzle1.globs)
    GraphicsObject.generate()
