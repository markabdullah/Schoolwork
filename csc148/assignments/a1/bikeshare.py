"""Assignment 1 - Bike-share objects

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto


=== Module Description ===

This file contains the Station and Ride classes, which store the data for the
objects in this simulation.

There is also an abstract Drawable class that is the superclass for both
Station and Ride. It enables the simulation to visualize these objects in
a graphical window.
"""
from datetime import datetime
from typing import Tuple

# Sprite files
STATION_SPRITE = 'stationsprite.png'
RIDE_SPRITE = 'bikesprite.png'


class Drawable:
    """A base class for objects that the graphical renderer can be drawn.

    === Public Attributes ===
    sprite:
        The filename of the image to be drawn for this object.
    """
    sprite: str

    def __init__(self, sprite_file: str) -> None:
        """Initialize this drawable object with the given sprite file.
        """
        self.sprite = sprite_file

    def get_position(self, time: datetime) -> Tuple[float, float]:
        """Return the (long, lat) position of this object at the given time.
        """
        raise NotImplementedError


class Station(Drawable):
    """A Bixi station.

    === Public Attributes ===
    location:
        the location of the station in lat/long coordinates
    capacity:
        the total number of bikes the station can store
    num_bikes: int
        current number of bikes at the station
    name: str
        name of the station
    rides_started: int
        number of rides that started at this station
    rides_ended: int
        number of rides that ended at this station
    low_availability: datetime
        total ammount of time in seconds this station spent with at most 5 bikes
    low_unoccupied: datetime
        total ammount of time in seconds this station spend with at most 5
        unoccupied spots

    === Representation Invariants ===
    - 0 <= num_bikes <= capacity
    - rides_started >= 0
    - rides_ended >= 0
    """

    location: Tuple[float, float]
    capacity: int
    num_bikes: int
    name: str
    rides_started: int
    rides_ended: int
    low_availability: int
    low_unoccupied: int

    def __init__(self, pos: Tuple[float, float], cap: int,
                 num_bikes: int, name: str) -> None:
        """Initialize a new station.

        Precondition: 0 <= num_bikes <= cap
        """
        super(Station, self).__init__(STATION_SPRITE)
        self.location = pos
        self.capacity = cap
        self.num_bikes = num_bikes
        self.name = name
        self.rides_started = 0
        self.rides_ended = 0
        self.low_availability = 0
        self.low_unoccupied = 0

    def get_position(self, time: datetime) -> Tuple[float, float]:
        """Return the (long, lat) position of this station for the given time.

        Note that the station's location does *not* change over time.
        The <time> parameter is included only because we should not change
        the header of an overridden method.
        """
        return (self.location[0], self.location[1])


class Ride(Drawable):
    """A ride using a Bixi bike.

    === Attributes ===
    start:
        the station where this ride starts
    end:
        the station where this ride ends
    start_time:
        the time this ride starts
    end_time:
        the time this ride ends

    === Representation Invariants ===
    - start_time < end_time
    """
    start: Station
    end: Station
    start_time: datetime
    end_time: datetime

    def __init__(self, start: Station, end: Station,
                 times: Tuple[datetime, datetime]) -> None:
        """Initialize a ride object with the given start and end information.
        """
        super(Ride, self).__init__(RIDE_SPRITE)
        self.start, self.end = start, end
        self.start_time, self.end_time = times[0], times[1]

    def get_position(self, time: datetime) -> Tuple[float, float]:
        """Return the (long, lat) position of this ride for the given time.

        A ride travels in a straight line between its start and end stations
        at a constant speed.

        === Preconditions ===
        self.start_time <= time <= self.end_time
        """
        # Number of mins the ride takes and mins past since the ride started
        ride_mins = (self.end_time - self.start_time).total_seconds() / 60
        mins_past = (time - self.start_time).total_seconds() / 60

        # Calculating the distance traveled in long/lat per minute
        diff_long = (self.end.location[0] - self.start.location[0]) / ride_mins
        diff_lat = (self.end.location[1] - self.start.location[1]) / ride_mins

        # Calculating current long/lat as start position plus the distance
        # traveled for each minute past the start time
        current_long = self.start.location[0] + diff_long * mins_past
        current_lat = self.start.location[1] + diff_lat * mins_past

        return (current_long, current_lat)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'doctest', 'python_ta', 'typing',
            'datetime'],
        'max-attributes': 15
    })
