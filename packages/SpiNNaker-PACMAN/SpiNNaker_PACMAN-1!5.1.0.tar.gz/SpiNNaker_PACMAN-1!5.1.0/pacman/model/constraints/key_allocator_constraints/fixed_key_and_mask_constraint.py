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

from .abstract_key_allocator_constraint import AbstractKeyAllocatorConstraint
from pacman.model.routing_info import BaseKeyAndMask
from pacman.exceptions import PacmanConfigurationException


class FixedKeyAndMaskConstraint(AbstractKeyAllocatorConstraint):
    """ Key allocator constraint that fixes the key and mask of an edge.
    """

    __slots__ = [
        # The key and mask combinations to fix
        "_keys_and_masks",

        #  Optional function which will be called to translate the
        # keys_and_masks list into individual keys If missing, the keys will
        # be generated by iterating through the keys_and_masks list directly.
        #  The function parameters are:
        #           An iterable of keys and masks
        #           A machine edge
        #           Number of keys to generate (may be None)
        "_key_list_function"

    ]

    def __init__(self, keys_and_masks, key_list_function=None):
        """
        :param keys_and_masks: The key and mask combinations to fix
        :type keys_and_masks: \
            iterable(:py:class:`pacman.model.routing_info.BaseKeyAndMask`)
        :param key_list_function: Optional function which will be called to\
            translate the keys_and_masks list into individual keys. If\
            missing, the keys will be generated by iterating through the \
            keys_and_masks list directly. The function parameters are:
            * An iterable of keys and masks
            * A machine edge
            * Number of keys to generate (may be None)
        :type key_list_function: iterable(\
            :py:class:`pacman.model.routing_info.BaseKeyAndMask`,\
            :py:class:`pacman.model.graphs.machine.MachineEdge`,\
            int) -> iterable(int)
        """
        for keys_and_mask in keys_and_masks:
            if not isinstance(keys_and_mask, BaseKeyAndMask):
                raise PacmanConfigurationException(
                    "the keys and masks object contains a object that is not"
                    "a key_and_mask object")

        self._keys_and_masks = keys_and_masks
        self._key_list_function = key_list_function

    @property
    def keys_and_masks(self):
        """ The keys and masks to be fixed

        :return: An iterable of key and mask combinations
        :rtype: iterable(:py:class:`pacman.model.routing_info.BaseKeyAndMask`)
        """
        return self._keys_and_masks

    @property
    def key_list_function(self):
        """ A function to call to generate the keys

        :return: A python function, or None if the default function can be used
        """
        return self._key_list_function

    def __repr__(self):
        return (
            "FixedKeyAndMaskConstraint("
            "keys_and_masks={}, key_list_function={})".format(
                self._keys_and_masks, self.key_list_function))

    def __eq__(self, other):
        if not isinstance(other, FixedKeyAndMaskConstraint):
            return False
        if other.key_list_function != self._key_list_function:
            return False
        if len(self._keys_and_masks) != len(other.keys_and_masks):
            return False
        return all(km in other.keys_and_masks for km in self._keys_and_masks)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return (
            frozenset(self._keys_and_masks),
            self._key_list_function).__hash__()
