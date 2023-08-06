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


from __future__ import division

# numpy and scipy
import numpy as np
import os.path as osp
import logging
import tempfile
import shutil
import collections
import numbers

from openmodes.mesh import gmsh
from openmodes.integration import DunavantRule
from openmodes.parts import SinglePart, CompositePart, MultiPart
from openmodes.basis import LoopStarBasis, BasisContainer
from openmodes.operator import EfieOperator
from openmodes.visualise import plot_mayavi, write_vtk, preprocess
from openmodes.mesh import TriangularSurfaceMesh
from openmodes.helpers import Identified
from openmodes.material import FreeSpace, PecMaterial
from openmodes.modes import Modes
from openmodes.multipole import spherical_multipoles, multipole_fixed
from openmodes.constants import c
from openmodes.array import LookupArray


class Simulation(Identified):
    """This object controls everything within the simluation. It contains all
    the parts which have been placed, and the operator equation which is
    used to solve the scattering problem.
    """

    def __init__(self, integration_rule=DunavantRule(5),
                 basis_class=LoopStarBasis,
                 operator_class=EfieOperator,
                 impedance_class=None,
                 name=None,
                 basis_args=dict(),
                 background_material=FreeSpace,
                 notebook=False):
        """
        Parameters
        ----------
        integration_rule : integer
            the order of the integration rule on triangles
        basis_class : type
            The class representing the type of basis function which will be
            used
        impedance_class : type
            The class representing the type of impedance matrix
        operator_class : type
            The class representing the operator equation to be solved
        name : string, optional
            A name for this simulation
        basis_args: dictionary, optional
            Arguments to be passed when constructing basis functions
        background_material: IsotropicMaterial, optional
            The material containing all simulation objects. Please note that
            background materials other than free space have not been fully
            tested yet, so YMMV.
        notebook: boolean, optional
            If True, then produce nicer output, which requires that the
            simulation is running within the Jupyter (IPython) notebook
        """

        super(Simulation, self).__init__()

        if name is None:
            name = str(self.id)

        self.integration_rule = integration_rule

        self.parts = CompositePart()

        self.basis_class = basis_class
        self.background_material = background_material
        self.basis_container = BasisContainer(basis_class, basis_args)
        self.operator = operator_class(integration_rule=integration_rule,
                                       basis_container=self.basis_container,
                                       background_material=background_material,
                                       impedance_class=impedance_class)

        self.multipole_cache = {}
        self.notebook = notebook
        if notebook:
            from openmodes.ipython import init_3d
            init_3d()

        logging.info('Creating simulation %s\nQuadrature order %d\n'
                     'Basis function class %s'
                     % (name, integration_rule.order, basis_class))

    def place_part(self, mesh=None, parent=None, location=None,
                   material=PecMaterial):
        """Add a part to the simulation domain

        Parameters
        ----------
        mesh : an appropriate mesh object, optional
            If specified, an individual part will be placed, otherwise an
            empty composite part will be created
        parent : CompositePart, optional
            If specified, the part will be a child of some composite part
        location : array, optional
            If specified, place the part at a given location, otherwise it will
            be placed at the origin
        material : IsotropicMaterial, optional,
            The material of this part. If not specified, will default to PEC

        Returns
        -------
        part : Part
            The part placed in the simulation

        The part will be placed at the origin. It can be translated, rotated
        etc using the relevant methods of `Part`
        """

        if mesh is None:
            part = CompositePart(location)
        else:
            part = SinglePart(mesh, location=location, material=material)

        # if not parent specified, use the root part of the simulation
        parent = parent or self.parts
        if not isinstance(parent, CompositePart):
            raise ValueError("Can only add a part to a composite part")

        parent.add_part(part)

        return part

    def iter_freqs(self, freqs, log_skip=10, log_label="Sweep frequency"):
        """Return an iterator over a range of frequencies

        It is possible to nest multiple frequency iterators, e.g. to sweep
        both real and imaginary parts of frequency.

        Parameters
        ----------
        freqs : array or list
            All the frequencies over which to iterate, in Hz
        log_skip : integer, optional
            How many frequencies to skip between logging calls. Set this very
            large to avoid all logging.
        log_label : string, optional
            The logging output string, denoting this sweep

        Returns
        -------
        freq_iter : generator
            An iterator, which yields the frequency count and the complex
            frequency `s` for each frequency in the range. It also logs the
            frequency sweep.
        """

        if self.notebook:
            from .ipython import progress_iterator
            it = progress_iterator(freqs, description="Frequency Sweep")
            logging.info(log_label+" started")
            for freq_count, freq in enumerate(it):
                yield freq_count, 2j*np.pi*freq
            logging.info(log_label+" finished")
        else:
            num_freqs = len(freqs)
            for freq_count, freq in enumerate(freqs):
                if freq_count % log_skip == 0 and freq_count != 0:
                    logging.info(log_label+" %d/%d" % (freq_count, num_freqs))
                yield freq_count, 2j*np.pi*freq

    def impedance(self, s, parent=None):
        """Evaluate the self and mutual impedances of all parts in the
        simulation. Return an `ImpedancePart` object which can calculate
        several derived impedance quantities

        Parameters
        ----------
        s : number
            Complex frequency at which to calculate impedance (in rad/s)
        parent : Part, optional
            If specified, then only this part and its sub-parts will be
            calculated

        Returns
        -------
        impedance_matrices : ImpedanceParts
            The impedance matrix object which can represent the impedance of
            the object in several ways.
        """

        parent = parent or self.parts
        return self.operator.impedance(s, parent, parent)

    def source_vector(self, source_field, s, parent=None,
                      extinction_field=False):
        """Evaluate the source vectors due to an incident field, returning
        separate vectors for each part.

        Relevant objects describing incident fields can be constructed from
        the classes found in `openmodes.sources`

        Parameters
        ----------
        source_field: source object
            The object specifying the source field for arbitrary frequencies
        s: complex
            The frequency at which to evaluate the source
        parent : Part, optional
            If specified, then only this part and its sub-parts will be
            calculated
        extinction_field : boolean, optional
            If True, instead of the source field vector, return the vector
            used to calculate extinction for asymmetric operators.

        Returns
        -------
        V : LookupArray
            The source vector, which can be indexed by `Part` objects to find
            the field on each part.
        """

        parent = parent or self.parts
        return self.operator.source_vector(source_field, s, parent,
                                           extinction_field)

    def estimate_poles(self, contour, parts=None, threshold=1e-14,
                       previous_result=None, cauchy_integral=True, modes=None,
                       **kwargs):
        """Estimate the location of poles and their modes by Cauchy integration
        or a simpler quasi-static method

        Parameters
        ----------
        contour: Contour
            The object describing the complex integration contour
        parts: Part or list, optional
            Which particular part or parts to calculate poles for. If not
            specified, then the whole system will be used

        Returns
        -------
        estimates: dict
            If a list of parts was specified, then a dictionary will be
            returned with the parts as keys, and the solutions as values.
            Otherwise a single solution is returned. The solution is always
            a dictionary
        """
        parts = parts or self.parts

        if isinstance(modes, numbers.Integral):
            modes = np.arange(modes)

        iter_wrap = self.__iter_wrap("Contour Integration")
        estimate = self.operator.estimate_poles

        if isinstance(parts, collections.Iterable):
            # a list of parts was given
            logging.info("Estimating poles of multiple parts")
            res = {}
            for part in parts:
                # Only calculate parts which are different by their unique_id
                if part.unique_id not in res:
                    if previous_result is None:
                        previous = None
                    else:
                        previous = previous_result.modes_of_parts[part.unique_id]
                    res[part.unique_id] = estimate(contour, part, threshold,
                                                   previous, cauchy_integral,
                                                   modes, iter_wrap=iter_wrap)

            # Find the parent part it it already exists, otherwise create a
            # MultiPart to hold the various parts
            # TODO: Look harder to find an existing parent part
            if set(parts) == set(self.parts.children):
                parent_part = self.parts
            else:
                parent_part = MultiPart(children=parts)
        else:
            logging.info("Estimating poles of a single part")
            if previous_result is not None:
                previous_result = previous_result.modes_of_parts[parts]
            res = {parts.unique_id: estimate(contour, parts, threshold,
                                             previous_result, cauchy_integral,
                                             modes, iter_wrap=iter_wrap)}
            parent_part = parts
            parts = [parts]
           
                                     
        return Modes(parent_part, parts, res, self.operator, self.basis_container)

    def refine_poles(self, estimates, rel_tol=1e-8, max_iter=40):
        """Refine the location of poles by iterative search

        Parameters
        ----------
        estimates: dict
            The result returned from estimate_poles

        Results
        -------
        refined: dict
            If a single part is considered, then this contains the modal
            solution for that part. Otherwise it is a dictionary with keys
            given by the parts
        """

        iter_wrap = self.__iter_wrap("Refining modes")
        # Multiple parts have been estimated
        refined = {}
        for part in estimates.parts:
            uid = part.unique_id
            if uid not in refined:
                refined[uid] = self.operator.refine_poles(estimates.modes_of_parts[uid],
                                                          part, rel_tol, max_iter, iter_wrap)

        return Modes(estimates.parent_part, estimates.parts, refined,
                     self.operator, self.basis_container)

    def empty_array(self, part=None, extra_dims=()):
        """
        Create an empty array of the appropriate size to contain solutions for
        all of the parts, or a single part and its sub-parts

        Parameters
        ----------
        part : Part, optional
            The part for which to create the vector. If not specified, all
            parts in the full simulation
        extra_dims : tuple, optional
            This can give the sizes of additional dimensions
        """

        part = part or self.parts

        return LookupArray((self.operator.unknowns, (part, self.basis_container))+extra_dims, dtype=np.complex128)

    def plot_3d(self, solution=None, part=None, output_format='webgl',
                filename=None, compress_scalars=None,
                compress_separately=False, **kwargs):
        """Plot a solution on several parts

        Parameters
        ----------
        solution : array, optional
            The solution to plot, typically a vector of current. If not
            specified, then only the geometry will be plotted. Note that for
            all output formats except VTK, the particular current component
            ("J" or "M") must be explicitly selected
        part : Part, optional
            If specified, then only a particular part will be plotted
        output_format : string, optional
            The format of the output. Currently 'mayavi', 'vtk' or 'webgl'
        filename : string, optional
            If saving to a file, the name of the file to save to
        compress_scalars : real, optional
            Compression factor to change the dynamic range of the scalar
            solution, which will make the resulting plot easier to view, but
            less 'physically correct'
        compress_separately : boolean, optional
            If compressing dynamic range, do it separately for each part. This
            will conceal any difference in the relative strength of excitation
            between parts.
        """

        if part is None:
            if solution is None:
                part = part or self.parts
                basis_container = None
            else:
                # Use the parent part of the provided solution
                try:
                    part = solution.lookup[1][2]
                    basis_container = solution.lookup[1][1]
                except IndexError:
                    part = solution.lookup[0][2]
                    basis_container = solution.lookup[0][1]

        if output_format == 'vtk':
            write_vtk(part, filename, solution, basis_container)
            return

        if solution is None:
            # don't plot a solution, just plot a part
            parts_list = list(part.iter_single())
            charges = currents = centres = None
        else:
            parts_list, charges, currents, centres = preprocess(
                    part, solution, basis_container,
                    compress_scalars, compress_separately)

        output_format = output_format.lower()
        if output_format == 'mayavi':
            plot_mayavi(parts_list, charges, currents, vector_points=centres,
                        compress_scalars=compress_scalars, filename=filename)

        elif output_format == 'webgl':
            from openmodes.ipython import plot_3d
            return plot_3d(parts_list, charges, currents, centres,
                           **kwargs)
        else:
            raise ValueError("Unknown output format")

    def load_mesh(self, filename, mesh_tol=None, force_tuple=False, scale=None,
                  parameters={}, mesh_dir=None):
        """
        Open a geometry file and mesh it (or directly open a mesh file), then
        convert it into a mesh object. Note that the mesh is _not_ added to
        the simulation.

        Parameters
        ----------
        filename : string
            The name of the file to open. Can be a gmsh .msh file, or a gmsh
            geometry file, which will be meshed first
        mesh_tol : float, optional
            If opening a geometry file, it will be meshed with this tolerance
        force_tuple : boolean, optional
            Ensure that a tuple is always returned, even if only a single part
            is found in the file
        scale : real, optional
            A scaling factor to apply to all nodes, in case conversion between
            units is required. Note that `mesh_tol` is expressed in the
            original units of the geometry, before this scale factor is
            applied.
        parameters : dictionary, optional
            A dictionary containing geometric parameters to be overridden in
            a geometry file, before meshing
        mesh_dir : string, optional
            If specified, then the mesh will be created in this directory,
            and it will be preserved after creation. Otherwise a temporary
            directory will be created, which will be deleted after the mesh
            has been loaded. This parameter is only used if a geometry file is
            given which needs to be meshed

        Returns
        -------
        parts : tuple
            A tuple of mesh objects, one for each separate geometric
            entity found in the gmsh file

        Currently only `TriangularSurfaceMesh` objects are created
        """

        delete_dir = False
        if osp.splitext(osp.basename(filename))[1] == ".msh":
            # assume that this is a binary mesh already generate by gmsh
            meshed_name = filename
            if parameters != {}:
                raise ValueError("Cannot modify parameters of existing mesh")
        else:
            # assume that this is a gmsh geometry file, so mesh it first
            if mesh_dir is None:
                mesh_dir = tempfile.mkdtemp()
                delete_dir = True

            logging.info("Meshing geometry %s with parameters %s in dir %s"
                         % (filename, str(parameters), mesh_dir))
            meshed_name = gmsh.mesh_geometry(filename, mesh_dir, mesh_tol,
                                             parameters=parameters)

        logging.info("Loading mesh %s" % meshed_name)
        raw_mesh = gmsh.read_mesh_meshio(meshed_name)

        if delete_dir:
            shutil.rmtree(mesh_dir)

        parts = tuple(TriangularSurfaceMesh(sub_mesh, scale=scale)
                      for sub_mesh in raw_mesh)
        if len(parts) == 1 and not force_tuple:
            return parts[0]
        else:
            return parts

    def multipole_decomposition(self, solution, order, s, origin=None):
        """
        Perform a multipole decomposition of a current distribution

        Currently only spherical multipole decomposition is supported. The
        absolute phase of these coefficients has not been checked, but relative
        phase between electric and magnetic should produce correct scattering
        cross-section.

        Parameters
        ----------
        solution : LookupArray
            The solution to decompose. It must include electric current "J",
            and may optionally also include magnetic current "M".
        order: integer
            The order of the multipole expansion to perform
        s : complex
            The complex frequency at which to perform the decomposition
        origin : array (len 3), optional
            The origin about which to calculate the expansion. If not
            specified, the global coordinate origin is used.

        Returns
        -------
        a_e, a_m : complex arrays of size (order+1, 2*order+1)
            The spherical multipole coefficients, with indices l, m.
            Note that vales of |m| > l are invalid, so these parts of the
            arrays are undefined. Negative m are obtained with negative
            array indices.
        """
        container, parent_part = solution.lookup[1][1:]

        a_e = np.zeros((order+1, 2*order+1), np.complex128)
        a_m = np.zeros_like(a_e)

        k = (s/c/1j)
        if np.isreal(k):
            # Suppress false warnings when dropping an imaginary part of 0
            k = k.real

        for part in parent_part.iter_single():
            basis = self.basis_container[part]

            points, current_J = basis.interpolate_function(solution["J", part].simple_view(),
                                                           int_weight=True, integration_rule=self.integration_rule,
                                                           nodes=part.nodes)
            try:
                points, current_M = basis.interpolate_function(solution["M", part].simple_view(),
                                                               int_weight=True, integration_rule=self.integration_rule,
                                                               nodes=part.nodes)
            except KeyError:
                current_M = np.zeros_like(current_J)

            if origin is not None:
                points -= origin

            cache_key = (part.position_hash, order)
            try:
                fixed_terms = self.multipole_cache[cache_key]
            except KeyError:
                fixed_terms = multipole_fixed(order, points)
                self.multipole_cache[cache_key] = fixed_terms

            n_e, n_m = spherical_multipoles(order, k, points, current_J,
                                            1j*current_M,
                                            self.background_material.eta(s),
                                            fixed_terms)
            a_e += n_e
            a_m += n_m

        return a_e, a_m

    def __iter_wrap(self, description):
        "Generate a wrapper iterator if using the notebook"
        if self.notebook:
            from .ipython import progress_iterator
            return lambda x: progress_iterator(x, description=description)
        else:
            return lambda x: x
