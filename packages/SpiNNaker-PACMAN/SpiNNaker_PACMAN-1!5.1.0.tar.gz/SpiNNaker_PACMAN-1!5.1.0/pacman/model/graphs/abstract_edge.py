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
from spinn_utilities.abstract_base import AbstractBase, abstractproperty


@add_metaclass(AbstractBase)
class AbstractEdge(object):
    """ A directed edge in a graph between two vertices.
    """

    __slots__ = ()

    @abstractproperty
    def label(self):
        """ The label of the edge

        :return: The label
        :rtype: str
        :raise None: Raises no known exceptions
        """

    @abstractproperty
    def pre_vertex(self):
        """ The vertex at the start of the edge

        :rtype: :py:class:`pacman.model.graphs.abstract_vertex.AbstractVertex`
        """

    @abstractproperty
    def post_vertex(self):
        """ The vertex at the end of the edge

        :rtype: :py:class:`pacman.model.graphs.abstract_vertex.AbstractVertex`
        """

    @abstractproperty
    def traffic_type(self):
        """ The traffic type of the edge

        :rtype:\
            :py:class:`pacman.model.graphs.common.edge_traffic_type.EdgeTrafficType`
        """
