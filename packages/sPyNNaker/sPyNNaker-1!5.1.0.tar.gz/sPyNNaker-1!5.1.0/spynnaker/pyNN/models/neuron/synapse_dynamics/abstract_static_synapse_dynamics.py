# Copyright (c) 2017-2019 The University of Manchester
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from six import add_metaclass
from spinn_utilities.abstract_base import AbstractBase, abstractmethod
from .abstract_synapse_dynamics import AbstractSynapseDynamics


@add_metaclass(AbstractBase)
class AbstractStaticSynapseDynamics(AbstractSynapseDynamics):
    """ Dynamics which don't change over time.
    """
    # pylint: disable=too-many-arguments

    __slots__ = ()

    @abstractmethod
    def get_n_words_for_static_connections(self, n_connections):
        """ Get the number of 32-bit words for n_connections in a single row
        """

    @abstractmethod
    def get_static_synaptic_data(
            self, connections, connection_row_indices, n_rows,
            post_vertex_slice, n_synapse_types):
        """ Get the fixed-fixed data for each row, and lengths for the\
            fixed-fixed parts of each row.

        Data is returned as an array made up of an array of 32-bit words for\
        each row for the fixed-fixed region. The row into which connection\
        should go is given by connection_row_indices, and the total number of\
        rows is given by n_rows.

        Lengths are returned as an array made up of an integer for each row,\
        for the fixed-fixed region.
        """

    @abstractmethod
    def get_n_static_words_per_row(self, ff_size):
        """ Get the number of bytes to be read per row for the static data\
            given the size that was written to each row
        """

    @abstractmethod
    def get_n_synapses_in_rows(self, ff_size):
        """ Get the number of synapses in the rows with sizes ff_size
        """

    @abstractmethod
    def read_static_synaptic_data(
            self, post_vertex_slice, n_synapse_types, ff_size, ff_data):
        """ Read the connections from the words of data in ff_data
        """
