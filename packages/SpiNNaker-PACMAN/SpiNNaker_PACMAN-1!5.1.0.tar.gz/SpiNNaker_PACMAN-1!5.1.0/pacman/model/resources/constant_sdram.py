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

from .abstract_sdram import AbstractSDRAM


class ConstantSDRAM(AbstractSDRAM):
    """ Represents an amount of SDRAM used  on a chip in the machine.

    This is used when the amount of SDRAM needed is not effected by runtime
    """

    __slots__ = [
        # The amount of SDRAM in bytes
        "_sdram"
    ]

    def __init__(self, sdram):
        """
        :param sdram: The amount of SDRAM in bytes
        :type sdram: int
        :raise None: No known exceptions are raised
        """
        self._sdram = sdram

    def get_total_sdram(self, n_timesteps):
        return self._sdram

    @property
    def fixed(self):
        return self._sdram

    @property
    def per_timestep(self):
        return 0

    def __add__(self, other):
        if isinstance(other, ConstantSDRAM):
            return ConstantSDRAM(
                self._sdram + other._sdram)
        else:
            # The other is more complex so delegate to it
            return other.__add__(self)

    def __sub__(self, other):
        if isinstance(other, ConstantSDRAM):
            return ConstantSDRAM(
                self._sdram - other._sdram)
        else:
            # The other is more complex so delegate to it
            return other.sub_from(self)

    def sub_from(self, other):
        if isinstance(other, ConstantSDRAM):
            return ConstantSDRAM(
                other._sdram - self._sdram)
        else:
            # The other is more complex so delegate to it
            return other - self
