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
"""
Integration routines and quadrature rules over triangles
"""

import numpy as np
import numpy.linalg as la
import scipy.special


from openmodes.helpers import Identified
from openmodes.external.point_in_polygon import wn_PnPoly


class IntegrationRule(Identified):
    def __len__(self):
        return len(self.points)

    def __repr__(self):
        return "%s.%s(%d)" % (type(self).__module__, type(self).__name__,
                              self.order)

    def __iter__(self):
        "Iterate over all integration points and weights"
        for point, w in zip(self.points, self.weights):
            yield point, w


class DunavantRule(IntegrationRule):
    """The symmetric quadrature rule over a triangle as given in
    D. A. Dunavant, Int. J. Numer. Methods Eng. 21, 1129 (1985).

    xi_eta: array
        The barycentric coordinates (xi, eta) of the quadrature points
    weights: array
        The weights, normalised to sum to 1/2
    """

    def __init__(self, order):
        """Calculate the coefficients of the integration rule

        Parameters
        ----------
        order : integer
            The order of the rule (maximum 20)
        """
        super(DunavantRule, self).__init__()

        from openmodes import dunavant

        self.order = order
        num_points = dunavant.dunavant_order_num(order)
        xi_eta, weights = dunavant.dunavant_rule(order, num_points)

        self.points = np.asfortranarray(xi_eta.T)
        # scale the weights to 0.5
        self.weights = np.asfortranarray((weights*0.5/sum(weights)).T)

# This makes a useful default e.g. for interpolation
triangle_centres = DunavantRule(1)


class GaussLegendreRule(IntegrationRule):
    """1D Gauss Legendre Quadrature Rule

    Defined over the range (0, 1)
    """
    def __init__(self, order):
        "Weights and abscissae of Gauss-Legendre quadrature of order N"
        super(GaussLegendreRule, self).__init__()
        a = scipy.special.sh_legendre(order).weights

        self.weights = a[:, 1].real
        self.points = a[:, 0].real


class TrapezoidalRule(IntegrationRule):
    """1D Trapezoidal rule with evenly spaced points

    Defined over the range (0, 1)

    Includes the end-points
    """
    def __init__(self, order):
        super(TrapezoidalRule, self).__init__()

        self.points = np.linspace(0.0, 1.0, order+1)
        self.weights = np.ones(order+1)
        self.weights[0] *= 0.5
        self.weights[-1] *= 0.5


def cartesian_to_barycentric(r, nodes):
    """Convert cartesian coordinates to barycentric (area coordinates) in a
    triangle

    r - Nx2 array of cartesian coordinates
    nodes - 3x2 array of nodes of the triangle
    """

    T = np.array(((nodes[0, 0] - nodes[2, 0], nodes[1, 0] - nodes[2, 0]),
                 (nodes[0, 1] - nodes[2, 1], nodes[1, 1] - nodes[2, 1])))

    bary_coords = np.empty((len(r), 3))
    bary_coords[:, :2] = la.solve(T, (r[:, :2]-nodes[None, 2, :2]).T).T
    bary_coords[:, 2] = 1.0 - bary_coords[:, 1] - bary_coords[:, 0]
    return bary_coords


def triangle_electric_dipole(vertices, xi_eta, weights):
    """Calculate the dipole moment of a triangle with constant unit charge

    Parameters
    ----------
    vertices : ndarray
        the vertices which define the triangle
    xi_eta : ndarray
        the points of the quadrature rule in barycentric form
    weights : ndarray
        the weights of the integration

    Returns
    -------
    p : ndarray
        the electric dipole moment of the triangle
    """

    r = ((vertices[0]-vertices[2])*xi_eta[:, 0, None] +
         (vertices[1]-vertices[2])*xi_eta[:, 1, None] +
         vertices[2])

    return np.sum(weights[0, :, None]*r, axis=0)


def sphere_fibonacci(num_points, cartesian=False):
    """Compute points on the surface of a sphere based on the Fibonacci spiral

    Parameters
    ----------
    num_points : integer
        The number of points to place on the sphere
    cartesian : boolean, optional
        If True, cartesian coordinates will be returned instead of spherical

    Returns
    -------
    phi, theta : array (if `cartesian` is False)
        The polar and azimuthal angles of the points
    x, y, z : array (if `cartesian` is True)
        The cartesian coordinates of the points

    Algorithm from:
    R. Swinbank and R. James Purser, “Fibonacci grids: A novel approach to
    global modelling,” Q. J. R. Meteorol. Soc., vol. 132, no. 619, pp.
    1769–1793, Jul. 2006.
    """

    n = num_points

    phi = 0.5*(1 + np.sqrt(5))
    i = -n+1 + 2*np.arange(num_points, dtype=np.float64)

    theta = 2*np.pi*i / phi

    sphi = i/n
    cphi = np.sqrt((n + i) * (n - i)) / n

    if cartesian:
        x = cphi * np.sin(theta)
        y = cphi * np.cos(theta)
        z = sphi
        return x, y, z
    else:
        phi = np.arctan2(sphi, cphi)
        return theta, phi


class Contour(object):
    """A contour for line integration in the complex plane"""

    def points_inside(self, points):
        "Check each point to see whether it lies within the contour"
        vertices = np.array([x for x, w in self])
        vertices = np.hstack((vertices.real[:, None], vertices.imag[:, None]))
        inside = np.empty(np.product(points.shape), dtype=np.bool)

        for point_num, point in enumerate(points.flat):
            inside[point_num] = wn_PnPoly((point.real, point.imag), vertices)

        return inside


class CircularContour(Contour):
    """A circular contour in the complex frequency plane"""
    def __init__(self, centre, radius, integration_rule=TrapezoidalRule(20)):
        self.centre = centre
        self.radius = radius
        self.integration_rule = integration_rule

    def __iter__(self):
        d_theta = 2*np.pi
        for x, w in self.integration_rule:
            theta = 2*np.pi*x
            s = np.exp(1j*theta)*self.radius+self.centre
            ds_dtheta = 1j*np.exp(1j*theta)*self.radius
            yield(s, w*ds_dtheta*d_theta)

    def __len__(self):
        return len(self.integration_rule)


class RectangularContour(Contour):
    """A rectangular contour in the complex frequency plane"""
    def __init__(self, s_min, s_max, integration_rule=GaussLegendreRule(20)):
        """
        Parameters
        ----------
        s_min, s_max: complex
            The corners of the rectangle
        """
        min_real, max_real = sorted((s_min.real, s_max.real))
        min_imag, max_imag = sorted((s_min.imag, s_max.imag))

        self.integration_rule = integration_rule
        self.coordinates = (min_real+1j*min_imag, max_real+1j*min_imag,
                            max_real+1j*max_imag, min_real+1j*max_imag)

    def __iter__(self):
        """
        Returns
        -------
        gen: generator
            A generator which yields (s, w), where s is the complex frequency
            and w is the integration weight
        """
        # integrate over all 4 lines
        for line_count in range(4):
            s_start = self.coordinates[line_count]
            s_end = self.coordinates[(line_count+1) % 4]

            ds = s_end-s_start
            for x, w in self.integration_rule:
                s = s_start + ds*x
                yield(s, w*ds)

    def __len__(self):
        return 4*len(self.integration_rule)


class ExternalModeContour(Contour):
    """A modified rectangular contour which finds external modes of objects,
    including on the negative real axis, but avoids internal modes on the
    imaginary axis, and takes a detour about the origin"""
    def __init__(self, corner, integration_rule=GaussLegendreRule(20),
                 overlap_axes=None, avoid_origin=None):
        """
        Parameters
        ----------
        corner: complex
            The furthest corner of the complex plane. Must have positive
            imaginary and negative real parts
        overlap_axes: real, optional
            The amount by which to overlap the real axis, and to avoid the
            imaginary axis
        avoid_origin: real, optional
            The radius by which to skirt around the origin
        """
        if corner.real >= 0.0 or corner.imag <= 0.0:
            raise ValueError("Corner frequency must have negative real "
                             "and positive imaginary parts")

        corner_dimension = max(abs(corner.real), abs(corner.imag))

        if overlap_axes is None:
            overlap_axes = 1e-2*corner_dimension

        if avoid_origin is None:
            avoid_origin = 3e-2*corner_dimension

        if avoid_origin < overlap_axes or overlap_axes < 0:
            raise ValueError("Invalid contour shape")

        cos_avoid = np.sqrt(avoid_origin**2-overlap_axes**2)

        self.integration_rule = integration_rule
        self.coordinates = (-overlap_axes+1j*cos_avoid,
                            -overlap_axes+1j*corner.imag,
                            corner,
                            corner.real-1j*overlap_axes,
                            -cos_avoid-1j*overlap_axes
                            )
        self.avoid_angle = np.arcsin(overlap_axes/avoid_origin)
        self.avoid_origin = avoid_origin

    def __iter__(self):
        """
        Returns
        -------
        gen: generator
            A generator which yields (s, w), where s is the complex frequency
            and w is the integration weight
        """
        # integrate over all 4 straight lines
        for line_count in range(4):
            s_start = self.coordinates[line_count]
            s_end = self.coordinates[line_count+1]

            ds = s_end-s_start
            for x, w in self.integration_rule:
                s = s_start + ds*x
                yield(s, w*ds)

        # the circular arc avoiding the origin
        t_start = np.pi*0.5+self.avoid_angle
        t_end = self.avoid_angle
        dt = t_end-t_start

        for x, w in self.integration_rule:
            t = t_start + dt*x
            s = self.avoid_origin*(-np.sin(t) + 1j*np.cos(t))
            ds_dt = self.avoid_origin*(-np.cos(t) - 1j*np.sin(t))
            yield(s, w*ds_dt*dt)

    def __len__(self):
        return 5*len(self.integration_rule)


class EllipticalContour(Contour):
    """A quarter ellipse contour in the complex frequency plane"""
    def __init__(self, radius_real, radius_imag, offset_real, offset_imag,
                 integration_rule=GaussLegendreRule(20)):
        """
        Parameters
        ----------
        radius_real, radius_imag: real
            The radii of the real and imaginary parts. The signs of these
            determine which quadrant of the complex plane the quarter ellipse
            will be in
        offset_real, offset_imag: real
            The offsets of the straight line parts from the real and imaginary
            axes. Must be smaller in magnitude than the corresponding radii.
        """

        self.radius_real = radius_real
        self.radius_imag = radius_imag
        self.offset_imag = offset_imag
        self.offset_real = offset_real
        self.integration_rule = integration_rule

    def __iter__(self):
        """
        Returns
        -------
        gen: generator
            A generator which yields (s, w), where s is the complex frequency
            and w is the integration weight
        """
        radius_real = self.radius_real
        radius_imag = self.radius_imag
        offset_imag = self.offset_imag
        offset_real = self.offset_real

        # correct for the direction of rotation changing
        sign = -np.sign(radius_real/radius_imag)

        # the points of maximum real and imag (different from radius due to offsets)
        max_real = radius_real*np.sqrt(1.0 - (offset_imag/radius_imag)**2)
        max_imag = radius_imag*np.sqrt(1.0 - (offset_real/radius_real)**2)

        # the line parallel to the real axis
        s_start = max_real+1j*offset_imag
        s_end = offset_real+1j*offset_imag
        ds = s_end-s_start
        for x, w in self.integration_rule:
            s = s_start + ds*x
            yield(s, w*ds*sign)

        # the line parallel to the imaginary axis
        s_start = offset_real+1j*offset_imag
        s_end = offset_real+1j*max_imag
        ds = s_end-s_start
        for x, w in self.integration_rule:
            s = s_start + ds*x
            yield(s, w*ds*sign)

        # the elliptical segment
        t_start = np.arcsin(offset_real/radius_real)
        t_end = np.arccos(offset_imag/radius_imag)
        dt = t_end-t_start

        for x, w in self.integration_rule:
            t = t_start + dt*x
            s = radius_real*np.sin(t) + 1j*radius_imag*np.cos(t)
            ds_dt = radius_real*np.cos(t) - 1j*radius_imag*np.sin(t)
            yield(s, w*ds_dt*dt*sign)

    def __len__(self):
        return 3*len(self.integration_rule)
