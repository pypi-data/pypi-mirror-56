# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
#  OpenModes - An eigenmode solver for open electromagnetic resonantors
#  Copyright (C) 2013 David Powell
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#-----------------------------------------------------------------------------
"""This module contains most of the matrix construction routines which are
fully specific to RWG and related basis functions"""

import numpy as np

from openmodes.operator.singularities import singular_impedance_rwg
from openmodes.core import z_mfie_faces_self, z_mfie_faces_mutual
from openmodes.core import z_efie_faces_self, z_efie_faces_mutual
from openmodes.constants import pi, c


def impedance_curl_G(s, integration_rule, basis_o, nodes_o, basis_s, nodes_s,
                     normals, self_impedance, epsilon, mu, num_singular_terms,
                     singularity_accuracy, tangential_form):
    """Calculates the impedance matrix corresponding to the equation:
    fm . curl(G) . fn
    for RWG and related basis functions"""

    transform_o, _ = basis_o.transformation_matrices
    num_faces_o = len(basis_o.mesh.polygons)

    c_mat = c/np.sqrt(epsilon*mu)
    gamma_0 = s/c_mat

    if self_impedance:
        # calculate self impedance

        singular_terms = singular_impedance_rwg(basis_o,
                                                num_terms=num_singular_terms,
                                                rel_tol=singularity_accuracy,
                                                normals=normals)

        if tangential_form:
            singular_terms = singular_terms["T_MFIE"]
        else:
            singular_terms = singular_terms["N_MFIE"]

        if np.any(np.isnan(singular_terms[0])):
            raise ValueError("NaN returned in singular impedance terms")

        num_faces_s = num_faces_o
        res = z_mfie_faces_self(nodes_o, basis_o.mesh.polygons,
                                basis_o.mesh.polygon_areas, gamma_0,
                                integration_rule.points,
                                integration_rule.weights, normals,
                                tangential_form, *singular_terms)

        transform_s = transform_o

    else:
        # calculate mutual impedance
        num_faces_s = len(basis_s.mesh.polygons)

        res = z_mfie_faces_mutual(nodes_o, basis_o.mesh.polygons,
                                  nodes_s, basis_s.mesh.polygons,
                                  gamma_0, integration_rule.points,
                                  integration_rule.weights, normals,
                                  tangential_form)

        transform_s, _ = basis_s.transformation_matrices

    Z_faces, Z_dgamma_faces = res

    if np.any(np.isnan(Z_faces)):
        raise ValueError("NaN returned in impedance matrix")

    if np.any(np.isnan(Z_dgamma_faces)):
        raise ValueError("NaN returned in impedance matrix derivative")


    Z = transform_o.dot(transform_s.dot(Z_faces.reshape(num_faces_o*3,
                                                        num_faces_s*3,
                                                        order='C').T).T)

    Z_dgamma = transform_o.dot(transform_s.dot(Z_dgamma_faces.reshape(num_faces_o*3,
                                                        num_faces_s*3,
                                                        order='C').T).T)

    return Z, Z_dgamma/c_mat


def impedance_G(s, integration_rule, basis_o, nodes_o, basis_s, nodes_s,
                normals, self_impedance, epsilon, mu, num_singular_terms,
                singularity_accuracy, frequency_derivatives=False):
    """Calculates the impedance matrix corresponding to the equation:
    fm . (I + grad grad) G . fn
    for RWG or loop-star basis functions

    No factors of epsilon/mu are included, as these can vary depending on
    the operator
    """

    transform_L_o, transform_S_o = basis_o.transformation_matrices
    num_faces_o = len(basis_o.mesh.polygons)

    c_mat = c/np.sqrt(epsilon*mu)
    gamma_0 = s/c_mat

    if (self_impedance):
        # calculate self impedance

        singular_terms = singular_impedance_rwg(basis_o,
                                                num_terms=num_singular_terms,
                                                rel_tol=singularity_accuracy,
                                                normals=normals)
        singular_terms = singular_terms["T_EFIE"]
        if (np.any(np.isnan(singular_terms[0])) or
                np.any(np.isnan(singular_terms[1]))):
            raise ValueError("NaN returned in singular impedance terms")

        num_faces_s = num_faces_o
        res = z_efie_faces_self(nodes_o, basis_o.mesh.polygons, gamma_0,
                                integration_rule.points,
                                integration_rule.weights, *singular_terms)

        transform_L_s = transform_L_o
        transform_S_s = transform_S_o

    else:
        # calculate mutual impedance

        num_faces_s = len(basis_s.mesh.polygons)

        res = z_efie_faces_mutual(nodes_o, basis_o.mesh.polygons, nodes_s,
                                  basis_s.mesh.polygons, gamma_0,
                                  integration_rule.points,
                                  integration_rule.weights)

        transform_L_s, transform_S_s = basis_s.transformation_matrices

    A_faces, phi_faces, A_dgamma_faces, phi_dgamma_faces = res

    if np.any(np.isnan(A_faces)) or np.any(np.isnan(phi_faces)):
        raise ValueError("NaN returned in impedance matrix")

    if np.any(np.isnan(A_dgamma_faces)) or np.any(np.isnan(phi_dgamma_faces)):
        raise ValueError("NaN returned in impedance matrix derivative")

    L = transform_L_o.dot(transform_L_s.dot(A_faces.reshape(num_faces_o*3,
                                                            num_faces_s*3,
                                                            order='C').T).T)
    S = transform_S_o.dot(transform_S_s.dot(phi_faces.T).T)

    L /= 4*pi
    S /= pi

    if not frequency_derivatives:
        return L, S

    # transform the frequency derivatives
    dL_ds = transform_L_o.dot(transform_L_s.dot(A_dgamma_faces.reshape(num_faces_o*3,
                                                                num_faces_s*3,
                                                                order='C').T).T)
    dS_ds = transform_S_o.dot(transform_S_s.dot(phi_dgamma_faces.T).T)

    dL_ds /= c_mat*4*pi
    dS_ds /= c_mat*pi

    return L, S, dL_ds, dS_ds
