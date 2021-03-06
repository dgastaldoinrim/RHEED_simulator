import numpy as np
import pymatgen as mg
import numpy.ma as ma
from scipy import linalg
import warnings
import copy
import Errors

class Lattice():
    def __init__(self, space_group, lattice_parameters, elements, coordinates,miller_indexes,reconstruction):
        self._define_parameters_(space_group, lattice_parameters)
        self._define_elements_(elements)
        self._define_coordinates_(coordinates)
        self.lattice = mg.Lattice.from_parameters(self.a,self.b,self.c,self.alpha,self.beta,self.gamma)
        self.Amat = ma.masked_less_equal(self.lattice.matrix,10 ** (-15)).filled(0.)
        self.Bmat = ma.masked_less_equal(ma.masked_equal(self.lattice.reciprocal_lattice.matrix,-0.).filled(0.),10 ** (-15)).filled(0.)
        self.crystal = mg.Structure.from_spacegroup(self.space_group,self.lattice,self.elements,self.coordinates)
        self._define_base_(self.crystal.sites)
        self.kvec = np.dot(np.array(miller_indexes),self.Bmat)
        self._get_hkl_oriented_lattice_(self.kvec)
        self.reconstruction_string = reconstruction
        self._get_surface_(self.Amat, self.reconstruction_string)

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

    def _get_hkl_oriented_lattice_(self,kvec):
        if np.all(np.cross(kvec, np.array([0., 0., 1.])) == np.array([0., 0., 0.])):
            self.rotation_matrix = np.eye(3)
            self.rotAmat = self.Amat
            self.rotBmat = self.Bmat
            self.rotbase = self.base
        else:
            warnings.simplefilter("ignore")
            theta = - np.arctan(kvec[1] / kvec[0])
            phi = - np.arctan(np.sqrt(kvec[0] ** 2 + kvec[1] ** 2) / kvec[2])
            rthetaz = ma.masked_inside(ma.masked_equal(np.array([[np.cos(theta), -np.sin(theta), 0.],[np.sin(theta), np.cos(theta), 0.],[0., 0., 1.]]),-0.).filled(0.),-10 ** (-15),10 ** (-15)).filled(0.)
            rphiy = ma.masked_inside(ma.masked_equal(np.array([[np.cos(phi), 0., np.sin(phi)],[0., 1., 0.],[-np.sin(phi), 0., np.cos(phi)]]),-0.).filled(0.),-10 ** (-15),10 ** (-15)).filled(0.)
            matrix = np.dot(rphiy, rthetaz)
            rotkvec = ma.masked_inside(np.dot(matrix,kvec),-10 ** (-15),10 ** (-15)).filled(0.)
            Amattoreduce = np.dot(self.Amat, matrix)
            Ap, Al, Au = linalg.lu(Amattoreduce)
            Bmattoreduce = np.dot(self.Bmat, matrix)
            Bp, Bl, Bu = linalg.lu(Bmattoreduce)
            if np.all(np.cross(rotkvec, np.array([0., 0., 1.])) == np.array([0., 0., 0.])):
                self.rotation_matrix = matrix
                self.rotAmat = self._correct_u_matrices_(Au)
                self.rotBmat = self._correct_u_matrices_(Bu)
                self.rotbase = self._get_hkl_oriented_base_(matrix,self.base)

    def _correct_u_matrices_(self, matrix):
        corrected_matrix = []
        for row in matrix:
            if (row[0] < 0. or (row[0] == 0. and row[1] < 0.) or (row[0] == 0. and row[1] == 0. and row[2] < 0.)):
                corrected_matrix.append(ma.masked_equal(-row,-0.).filled(0.))
            else:
                corrected_matrix.append(row)
        return np.array(corrected_matrix)

    def _get_hkl_oriented_base_(self, rotation_matrix, base):
        rotated_base = copy.deepcopy(base)
        for key in base:
            vector = ma.masked_inside(np.dot(rotation_matrix,base[key]["Coordinates"]),-10 ** (-15),10 ** (-15)).filled(0.)
            rotated_base[key]["Coordinates"] = self._check_base_coordinates_(vector)
        return rotated_base

    def _check_base_coordinates_(self, vector):
        if vector[0] < 0:
            vector = vector + self.rotAmat[0]
            self._check_base_coordinates_(vector)
        elif vector[0] > self.rotAmat[0,0]:
            vector = vector - self.rotAmat[0]
            self._check_base_coordinates_(vector)
        if vector[1] < 0:
            vector = vector + self.rotAmat[1]
            self._check_base_coordinates_(vector)
        elif vector[1] > self.rotAmat[1,1]:
            vector = vector - self.rotAmat[1]
            self._check_base_coordinates_(vector)
        if vector[2] < 0:
            vector = vector + self.rotAmat[2]
            self._check_base_coordinates_(vector)
        elif vector[2] > self.rotAmat[2,2]:
            vector = vector - self.rotAmat[2]
            self._check_base_coordinates_(vector)
        if (vector >= 0.).all() and (vector <= np.array([self.rotAmat[0,0],self.rotAmat[1,1],self.rotAmat[2,2]])).all():
            return np.array(vector)
        else:
            self._check_base_coordinates_(vector)

    def _get_surface_(self, lattice, reconstruction):
        string_split = reconstruction.split('-')
        theta = float(string_split[2][1:])
        periodicities = string_split[1].split('X')
        p1, p2 = tuple([float(periodicities[0]),float(periodicities[1])])
        if string_split[0] == 'p':
            self.Woodsmatrix = ma.masked_inside(np.array([[np.cos(theta), - np.sin(theta)],[np.sin(theta), np.cos(theta)]]) * np.array([[p1, 0.],[0.,p2]]) * np.eye(2),-10 ** (-15),10 ** (-15)).filled(0.)
        else:
            self.Woodsmatrix = ma.masked_inside(np.array([[np.cos(theta), - np.sin(theta)],[np.sin(theta), np.cos(theta)]]) * np.array([[p1, 0.],[0.,p2]]) * np.array([[1., 0.],[0.5, 0.5]]),-10 ** (-15),10 ** (-15)).filled(0.)
        self.surfAmat = ma.masked_inside(self.Woodsmatrix * np.dot(np.array([[1., 0., 0.],[0., 1., 0.]]),np.dot(self.Amat, np.array([[1., 0.],[0., 1.],[0., 0.]]))),-10 ** (-15),10 ** (-15)).filled(0.)
        self.surfBmat = ma.masked_inside(2 * np.pi * np.transpose(linalg.inv(self.surfAmat)),-10 ** (-15),10 ** (-15)).filled(0.)