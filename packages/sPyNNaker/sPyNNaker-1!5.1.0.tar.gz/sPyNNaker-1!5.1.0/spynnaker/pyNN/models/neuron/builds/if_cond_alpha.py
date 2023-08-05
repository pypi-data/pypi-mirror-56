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

from spynnaker.pyNN.exceptions import SpynnakerException
from spynnaker.pyNN.models.defaults import defaults, default_initial_values


@defaults
class IFCondAlpha(object):
    """ Leaky integrate and fire neuron with an alpha-shaped current input.
    """

    # noinspection PyPep8Naming
    @default_initial_values({"v", "gsyn_exc", "gsyn_inh"})
    def __init__(
            self, tau_m=20, cm=1.0, e_rev_E=0.0, e_rev_I=-70.0, v_rest=-65.0,
            v_reset=-65.0, v_thresh=-50.0, tau_syn_E=0.3, tau_syn_I=0.5,
            tau_refrac=0.1, i_offset=0, v=-65.0, gsyn_exc=0.0, gsyn_inh=0.0):
        # pylint: disable=too-many-arguments, too-many-locals, unused-argument
        raise SpynnakerException(
            "This neuron model is currently not supported by the tool chain")
