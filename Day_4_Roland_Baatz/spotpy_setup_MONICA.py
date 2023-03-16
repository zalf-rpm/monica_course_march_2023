import numpy as np
import spotpy
import MONICA_adapter
import re

class spot_setup(object):
    def __init__(self, user_params, exp_maps, obslist):
        self.user_params = user_params
        self.params = []
        for par in user_params:
            parname = par["name"]
            if re.search(r'\d', par["array"]): #check if par["array"] contains numbers
                parname += "_" + par["array"] #spotpy does not allow two parameters to have the same name
            if "derive_function" not in par: #spotpy does not care about derived params
                self.params.append(spotpy.parameter.Uniform(parname, float(par["low"]), float(par["high"]), float(par["stepsize"]), float(par["optguess"]), float(par["minbound"]), float(par["maxbound"])))
        self.monica_model = MONICA_adapter.monica_adapter(exp_maps, obslist)

    def parameters(self):
        return spotpy.parameter.generate(self.params)

    def simulation(self, vector):
        #the vector comes from spotpy, self.user_params holds the information coming from csv file
        simulations = self.monica_model._run(vector, self.user_params)
        return simulations

    def evaluation(self):
        return self.monica_model.observations

    def objectivefunction(self,simulation,evaluation):
        objectivefunction= spotpy.objectivefunctions.rmse(evaluation,simulation)
        return objectivefunction
