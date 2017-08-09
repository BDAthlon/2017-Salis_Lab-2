# Input parser
# Ayaan Hossain

from collections import defaultdict
from itertools   import imap

def invalid_statement(message='check error line.'):
    raise Exception('Invalid statement(s) in program! Ref: {}'.format(' '.join(message)))

def get_parsed_struct(species, program):
    # Parse species
    species       = [statement.strip().split() for statement in species.strip().split('\n') if statement.strip()]
    def_dict_func = lambda: {'alpha':None, 'x0':None}
    def_dict      = defaultdict(def_dict_func)
    for definition in species:
        try:
            if not len(definition) == 3:
                return invalid_statement(definition)
            else:
                var, alpha, x0         = definition
                def_dict[var]['alpha'] = float(alpha)
                def_dict[var]['x0']    = float(x0)
        except:
            return invalid_statement(definition)

    # Parse program
    program         = [statement.strip().split() for statement in program.strip().split('\n') if statement.strip()]
    valid_action    = set(['represses', 'activates', 'inverts'])
    gc_dict_func_l3 = lambda: {'p':None,  't':None}
    gc_dict_func_l2 = lambda: {'kd':None, 'n':None}
    gc_dict_func_l1 = lambda: {'represses':defaultdict(gc_dict_func_l2), 'activates':defaultdict(gc_dict_func_l2), 'inverts':defaultdict(gc_dict_func_l3)}
    gc_dict         = defaultdict(gc_dict_func_l1)
    for statement in program:
        if len(statement) == 4:
            try:
                var_i, action, var_j, val_tuple = statement    
                val_i, val_j = imap(float, val_tuple[1:-1].split(','))
            except:
                return invalid_statement(statement)
            if not (action in valid_action and var_i in def_dict and var_j in def_dict):
                return invalid_statement(statement)
            e1, e2 = ('kd', 'n') if action != 'inverts' else ('p', 't')
            gc_dict[var_i][action][var_j][e1], gc_dict[var_i][action][var_j][e2] = val_i, val_j
        else:
            return invalid_statement(statement)

    return def_dict, gc_dict

def main():
    '''
    Circuit Globs Grammar
    Species: Statements of the form <var> <max_trans_rate> <init_conc>
    Program: Statements of the form <var_i> <action> <var_j> <(val_1, val_2)>
    Actions: Operations from <represses, activates, inverts>
    '''

    species = '''
    R1 100 1000
    R2 50 5000
    A1 90 9000
    I1 77 7700
    RFP 600 6000
    GFP 700 7000
    '''
    print species

    program = '''
    R1 represses GFP (5,1)
    R1 represses R2 (2,1)
    R2 represses R1 (0.7,2)
    A1 activates GFP (5,1)
    I1 inverts R2 (6,7)
    '''
    # C1 chaperones A1
    
    print program

    a, b = get_parsed_struct(species, program)

    print a
    print
    print b['R1']
    print b['R2']
    print b['A1']
    print b['I1']

if __name__ == '__main__':
    main()