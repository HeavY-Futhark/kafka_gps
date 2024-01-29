from __future__ import annotations
from typing import Type
import math
from datetime import datetime
from models.coordinate_model import Coordinate
import random
from global_land_mask import globe

def is_in_ocean(latitude: float, longitude: float) -> bool:
    """ Check whether if the given point is in the ocean or on land

    Parameters:
        latitude (float): Latitude of the point to check
        longitude (float): Longitude of the point to check

    Returns:
        (bool): True iff the given point is in the ocean

    Example:
    ```python
    assert(is_in_ocean(43, -23.5))
    assert(not(is_in_ocean(59, 80)))
    ```
    """
    return globe.is_ocean(latitude, longitude)

def _move_point(
    latitude: float,
    longitude: float,
    delta_latitude: float,
    delta_longitude: float
) -> tuple[float, float]:
    """ Moves a point from the given coordinate and following the given
    deplacement, keeping the coordinates value in their possible interval.

    Parameters:
        latitude (float): Latitude of the point to move
        longitude (float): Longitude of the point to move
        delta_latitude (float): Wanted deplacement for the latitude
        delta_longitude (float): Wanted deplacement for the longitude

    Returns:
        (tuple[float, float]): New latitude and longitude after the deplacement
    """
    new_latitude = latitude + delta_latitude
    new_latitude = (new_latitude + 90) % 180 - 90
    new_longitude = longitude + delta_longitude
    new_longitude = (new_longitude + 180) % 360 - 180
    return new_latitude, new_longitude


class CoordinateTracker:
    """ Moves a point randomly

    Attributes:
        ip (str): Ip of the tracker
        latitude (float): Current latitude of the point
        longitude (float): Current longitude of the point
        speed (float): Speed of the point
        direction (float): Angle of deplacement of the point
        max_angular_speed (float): Absolute value of the maximal angular speed
        of the point
        can_swim (bool): True iff the coordinates can be in the ocean

    Methods:
        update_position(self, float): Update the position to move the point
        during the given time
        get_coordinates(self): Returns the coordinates of the point
    """
    def __init__(
        self: Self,
        ip: str,
        initial_latitude: float,
        initial_longitude: float,
        speed: float,
        initial_direction: float,
        max_angular_speed: float,
        can_swim: bool
    ):
        """ Create a new CoordinateTracker with the given attributes

        Parameters:
            self (Self): Current instance
            ip (str): Ip of the tracker
            initial_latitude (float): Initial latitude of the point
            initial_longitude (float): Initial longitude of the point
            speed (float): Speed of the point
            initial_direction (float): Angle of deplacement of the point
            max_angular_speed (float): Absolute value of the maximal angular
            speed of the point
            can_swim (bool): True iff the coordinates can be in the ocean
        """
        self.ip = ip
        self.latitude = initial_latitude
        self.longitude = initial_longitude
        self.speed = speed
        self.direction = initial_direction
        self.max_angular_speed = max_angular_speed
        self.can_swim = can_swim

    def _rotate(self: Self):
        """ Rotate the point randomly

        Parameters:
            self (Self): Current instance
        """
        self.direction += random.uniform(-self.max_angular_speed, self.max_angular_speed)

    def _generate_speed(
        self: Self,
        direction_in_radians: float,
        time_elapsed: float
    ) -> tuple[float, float]:
        """ Determins the deplacement of the point with the given angle in the
        time elapsed

        Parameters:
            self (Self): Current instance
            direction_in_radians (float): Angle that the instance faces (in
            radians)
            time_elapsed (float): Time since the last deplacement

        Returns:
            tuple[float, float]: Deplacement of the point followint the
            latitude and the longitude
        """
        distance = self.speed * time_elapsed
        delta_latitude = distance * math.cos(direction_in_radians)
        delta_longitude = distance * math.sin(direction_in_radians)
        return delta_latitude, delta_longitude

    def update_position(self: Self, time_elapsed: float):
        """ Updates the position of the point

        Parameters:
            time_elapsed (float): Time elapsed since the last deplacement

        Example:
        ```python
        coordinateTracker = CoordinateTracker(
            ip = 'my_ip',
            initial_latitude = 0,
            initial_longitude = 0,
            speed = 0.02,
            initial_direction = 0,
            max_angular_speed = 45,
            can_swim = True
        )
        coordinateTracker.update_position(1)
        """
        self._rotate()
        delta_latitude, delta_longitude = self._generate_speed(
            direction_in_radians = math.radians(self.direction),
            time_elapsed = time_elapsed
        )
        new_latitude, new_longitude = _move_point(
            latitude = self.latitude,
            longitude = self.longitude,
            delta_latitude = delta_latitude,
            delta_longitude = delta_longitude
        )
        if self.can_swim or not(is_in_ocean(new_latitude, new_longitude)):
            self.latitude = new_latitude
            self.longitude = new_longitude
        else:
            self._bring_back_to_continent(
                wanted_delta_latitude = delta_latitude,
                wanted_delta_longitude = delta_longitude
            )

    def _bring_back_to_continent(
        self: Self,
        wanted_delta_latitude: float,
        wanted_delta_longitude: float
    ):
        """ Moves the point to keep it on land
        Invert the angle, tries to invert the given deplacement, and if the
        point would still be in the water, stay still

        Parameters:
            wanted_delta_latitude (float): Planned deplacement following the
            latitude
            wanted_delta_longitude (float): Planned deplacement following the
            longitude
        """
        self.direction = -self.direction
        position_if_reverse = _move_point(
            latitude = self.latitude,
            longitude = self.longitude,
            delta_latitude = -wanted_delta_latitude,
            delta_longitude = -wanted_delta_longitude
        )
        if not(is_in_ocean(*position_if_reverse)):
            self.latitude, self.longitude = position_if_reverse
        else:
            # The point does not move
            pass
        
        
    def get_coordinates(self: Self) -> Coordinate:
        """ Returns the coordinates of the point

        Parameters:
            self (Self): Current instance

        Returns:
            (Coordinate): Current coordinates of the point

        Example:
        ```python
        coordinateTracker = CoordinateTracker(
            ip = 'my_ip',
            initial_latitude = 0,
            initial_longitude = 0,
            speed = 0.02,
            initial_direction = 0,
            max_angular_speed = 45,
            can_swim = True
        )
        coordinate = coordinateTracker.get_coordinates()
        assert(coordinate.ip == 'my_ip')
        assert(coordinate.latitude == 0)
        assert(coordinate.longitude == 0)
        """
        # Renvoie les coordonnées actuelles
        return Coordinate(
            ip = self.ip,
            time = datetime.now(),
            latitude = self.latitude,
            longitude = self.longitude
        )
