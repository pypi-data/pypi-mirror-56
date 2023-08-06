#!/usr/bin/python3.7
"""
Copyright (C) 2019 Reinventing Geospatial, Inc.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>,
or write to the Free Software Foundation, Inc., 59 Temple Place -
Suite 330, Boston, MA 02111-1307, USA.

Author: Jenifer Cochran, Reinventing Geospatial Inc (RGi)
Date: 2019-19-9
Credits:
SWAGD implementation:
 https://gitlab.com/GitLabRGI/erdc/swagd/blob/master/swagd-common/src/main/java/com/rgi/common/tile/TileOrigin.java
Version:
"""

from astroid import Tuple

from nsg.common.enum_with_attributes import EnumWithAttributes


class TileOrigin(EnumWithAttributes):
    """Indicates the tile origin of a tile."""

    UPPER_LEFT = (0, 1)
    LOWER_LEFT = (0, 0)
    UPPER_RIGHT = (1, 1)
    LOWER_RIGHT = (1, 0)

    def __init__(self, horizontal: int, vertical: int):
        """
        constructor
        :param horizontal: the horizontal direction
        :param vertical: the vertical direction
        """
        self.horizontal = horizontal
        self.vertical = vertical


def _transform_horizontal(from_origin: TileOrigin,
                          to_origin: TileOrigin,
                          tile_x_coordinate: int,
                          matrix_width: int):
    return _transform(from_direction=from_origin.horizontal,
                      to_direction=to_origin.horizontal,
                      tile_coordinate=tile_x_coordinate,
                      matrix_dimension=matrix_width)


def _transform_vertical(from_origin: TileOrigin,
                        to_origin: TileOrigin,
                        tile_y_coordinate: int,
                        matrix_height: int):
    return _transform(from_direction=from_origin.vertical,
                      to_direction=to_origin.vertical,
                      tile_coordinate=tile_y_coordinate,
                      matrix_dimension=matrix_height)


def transform(from_origin: TileOrigin,
              to_origin: TileOrigin,
              tile_coordinate: Tuple(int),
              matrix_dimensions: Tuple(int)):
    """
    transforms the tile coordinate from one tile origin scheme to the to_origin tile origin scheme
    :param from_origin: The origin that the coordinate current is in
    :param to_origin: The origin that the coordinate will be transformed to
    :param tile_coordinate: the tile coordinate to transform
    :param matrix_dimensions: the dimensions of the tile matrix
    :return: the transformed tile coordinate (x,y) as a tuple
    """
    return _transform_horizontal(from_origin, to_origin, tile_coordinate[0], matrix_dimensions[0]), \
           _transform_vertical(from_origin, to_origin, tile_coordinate[1], matrix_dimensions[1])


def _transform(from_direction: int,
               to_direction: int,
               tile_coordinate: int,
               matrix_dimension: int):
    max_tile_coordinate = matrix_dimension - 1
    return tile_coordinate + (from_direction ^ to_direction) * (max_tile_coordinate - 2 * tile_coordinate)
