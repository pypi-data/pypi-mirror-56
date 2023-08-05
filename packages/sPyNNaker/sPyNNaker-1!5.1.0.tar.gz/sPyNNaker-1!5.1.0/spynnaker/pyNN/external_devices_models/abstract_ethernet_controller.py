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


@add_metaclass(AbstractBase)
class AbstractEthernetController(object):
    """ A controller that can send multicast packets which can be received\
        over Ethernet and translated to control an external device
    """
    __slots__ = ()

    @abstractmethod
    def get_message_translator(self):
        """ Get the translator of messages

        :rtype:\
            :py:class:`spynnaker.pyNN.external_devices_models.AbstractEthernetTranslator`
        """

    @abstractmethod
    def get_external_devices(self):
        """ Get the external devices that are to be controlled by the\
            controller
        """

    @abstractmethod
    def get_outgoing_partition_ids(self):
        """ Get the partition IDs of messages coming out of the controller

        :rtype: list(str)
        """
