import numpy as np
import pymatgen as mg
import numpy.ma as ma
import Errors

class Lattice():
    def __init__(self, space_group, lattice_parameters, elements, coordinates):
        self._define_parameters_(space_group, lattice_parameters)
        self._define_elements_(elements)
        self._define_coordinates_(coordinates)
        self.lattice = mg.Lattice.from_parameters(self.a,self.b,self.c,self.alpha,self.beta,self.gamma)
        self.Amat = ma.masked_less_equal(self.lattice.matrix,10 ** (-15)).filled(0.)
        self.Bmat = ma.masked_less_equal(ma.masked_equal(self.lattice.reciprocal_lattice.matrix,-0.).filled(0.),10 ** (-15)).filled(0.)
        self.crystal = mg.Structure.from_spacegroup(self.space_group,self.lattice,self.elements,self.coordinates)
        self._define_base_(self.crystal.sites)

    def _define_parameters_(self, space_group, parameters):
        try:
            if space_group > 0 and space_group < 3:
                try:
                    if len(parameters) == 6:
                        self.a = parameters[0]
                        self.b = parameters[1]
                        self.c = parameters[2]
                        self.alpha = parameters[3]
                        self.beta = parameters[4]
                        self.gamma = parameters[5]
                    else:
                        raise Errors.WrongParametersNumber(len(parameters), 6)
                except Errors.WrongParametersNumber() as error:
                    error.error_handler()
            elif space_group < 16:
                try:
                    if len(parameters) == 4:
                        self.a = parameters[0]
                        self.b = parameters[1]
                        self.c = parameters[2]
                        self.alpha = 90.
                        self.beta = parameters[3]
                        self.gamma = 90.
                    else:
                        raise Errors.WrongParametersNumber(len(parameters), 4)
                except Errors.WrongParametersNumber() as error:
                    error.error_handler()
            elif space_group < 75:
                try:
                    if len(parameters) == 3:
                        self.a = parameters[0]
                        self.b = parameters[1]
                        self.c = parameters[2]
                        self.alpha = 90.
                        self.beta = 90.
                        self.gamma = 90.
                    else:
                        raise Errors.WrongParametersNumber(len(parameters), 3)
                except Errors.WrongParametersNumber() as error:
                    error.error_handler
            elif space_group < 143:
                try:
                    if len(parameters) == 2:
                        self.a = parameters[0]
                        self.b = parameters[0]
                        self.c = parameters[1]
                        self.alpha = 90.
                        self.beta = 90.
                        self.gamma = 90.
                    else:
                        raise Errors.WrongParametersNumber(len(parameters), 2)
                except Errors.WrongParametersNumber as error:
                    error.error_handler()
            elif space_group < 168:
                try:
                    if len(parameters) == 4:
                        self.a = parameters[0]
                        self.b = parameters[0]
                        self.c = parameters[0]
                        self.alpha = parameters[1]
                        self.beta = parameters[2]
                        self.gamma = parameters[3]
                    else:
                        raise Errors.WrongParametersNumber(len(parameters), 4)
                except Errors.WrongParametersNumber() as error:
                    error.error_handler()
            elif space_group < 195:
                try:
                    if len(parameters) == 2:
                        self.a = parameters[0]
                        self.b = parameters[0]
                        self.c = parameters[1]
                        self.alpha = 90.
                        self.beta = 90.
                        self.gamma = 120.
                    else:
                        raise Errors.WrongParametersNumber(len(parameters), 2)
                except Errors.WrongParametersNumber() as error:
                    error.error_handler()
            elif space_group < 231:
                try:
                    if len(parameters) == 1:    
                        self.a = parameters[0]
                        self.b = parameters[0]
                        self.c = parameters[0]
                        self.alpha = 90.
                        self.beta = 90.
                        self.gamma = 90.
                    else:
                        raise Errors.WrongParametersNumber(len(parameters), 1)
                except Errors.WrongParametersNumber as error:
                    error.error_handler()
            else:
                raise Errors.WrongLatticeSimmetry(space_group)
            self.space_group = space_group
        except Errors.WrongLatticeSimmetry as error:
            error.error_handler()

    def _define_elements_(self, elements):
        if len(elements) == 1:
            self.elements = [mg.Element(elements[0])]
        else:
            elements_list = [mg.Element(elements[0])]
            for i in range(1,len(elements)):
                elements_list += mg.Element(elements[i])
            self.elements = elements_list

    def _define_coordinates_(self, coordinates):
        if len(coordinates) == 1:
            self.coordinates = [np.array(coordinates[0])]
        else:
            coordinates_list = [np.array(coordinates[0])]
            for i in range(1,len(coordinates)):
                coordinates_list = np.append(coordinates_list,np.array(elements[i]),axis = 1)
            self.coordinates = coordinates_list

    def _define_base_(self, sites):
        base = {}
        for site in sites:
            base[sites.index(site)] = {'Element': site.species.elements[0], 'Coordinates': ma.masked_less_equal(site.coords,10 ** (-15)).filled(0.)}
        self.base = base 