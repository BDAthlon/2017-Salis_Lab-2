from math import *
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from gcparser import get_parsed_struct

def Hill_Function_R(Kd,N,C):
    # Hill function for modeling repressors
    hill=1/(1+(N/Kd)**C)
    # print hill
    return hill

def Hill_Function_A(Kd,N,C):
    # Hill function for modeling activators
    hill=((N**C))/((Kd**C)+(N**C))
    return hill

class CircuitModel(object):

    def __init__(self,def_dict,con_dict):

        #internalizes inputs
        self.def_dict=def_dict
        self.con_dict=con_dict
        #sets hashtable keys for inline ode assembly
        self.Plist=[key for key in def_dict.keys()]
        self.number_of_protein_states=len(self.Plist)

    def run(self):

        #sets ODE variables
        self.init_con=[self.def_dict[i]['x0'] for i in self.Plist]
        self.tspan=10000
        #degradation rate
        self.d=log(2)/60.0
        #runs ODE
        self.Xnew=odeint(simulation_ODE, self.init_con,
            [x for x in range(self.tspan)], (self,))
        self.dt=[x for x in range(self.tspan)]
        # extracts reporter behavior
        self.reporters=[self.Plist[i] for i in range(self.number_of_protein_states) if self.Plist[i] in ['RFP','GFP','BFP']]
        self.reporter_values=[self.Xnew[:,i] for i in range(self.number_of_protein_states) if self.Plist[i] in ['RFP','GFP','BFP']]
        
        t, reporter_values = self._clean_output(self.dt,self.reporter_values)
        return t,self.reporters,reporter_values

    def _clean_output(self,t,reporter_values):

        time = np.array(t)/60.0 # conver to minutes
        dt = len(time)/1000
        time = time[0::dt*2]
        reporter_values[0] = reporter_values[0][0::dt]

        return t,reporter_values

    def graph(self):
        plt.figure()
        plt.plot(self.dt,self.reporter_values[0],'g-')
        plt.show()

def simulation_ODE(y, t, (glob)):
    #initializes ODEs
    dX_dt = np.zeros(glob.number_of_protein_states);
    # sets max transcripton rates
    for p in range(glob.number_of_protein_states):
        dX_dt[p]+=glob.def_dict[glob.Plist[p]]['alpha']
    for p in range(glob.number_of_protein_states):
        #applies hills
        b=glob.con_dict[glob.Plist[p]]
        for j in b.keys():
            if j == "activates":
                a=b['activates']
                for key in a.keys():
                    dX_dt[glob.Plist.index(key)]*=Hill_Function_A(a[key]['kd'],y[p],a[key]['n'])
            elif j == "represses":
                r=b['represses']
                for key in r.keys():
                    dX_dt[glob.Plist.index(key)]*=Hill_Function_R(r[key]['kd'],y[p],r[key]['n'])
            # flips invertase
            elif j == "inverts":
                i=b['inverts']
                for key in i.keys():
                    if i[key]['p']>0:
                        if i[key]['t']>y[p]:
                            dX_dt[glob.Plist.index(key)]*=0.00001
                    else:
                        if i[key]['t']<y[p]:
                            dX_dt[glob.Plist.index(key)]*=0.00001
        #adds degradation
    for p in range(glob.number_of_protein_states):
        dX_dt[p]-=glob.d*y[p]
    return dX_dt

if __name__=="__main__":

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

    a, b = get_parsed_struct(species, program)

    g=CircuitModel(a,b)
    g.run()
    g.graph()