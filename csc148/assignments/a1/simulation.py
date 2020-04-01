"""Assignment 1 - Simulation

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto


=== Module Description ===

This file contains the Simulation class, which is the main class for your
bike-share simulation.

At the bottom of the file, there is a sample_simulation function that you
can use to try running the simulation at any time.
"""
import csv
from datetime import datetime, timedelta
import json
from typing import Dict, List, Tuple

from bikeshare import Ride, Station
from container import PriorityQueue
from visualizer import Visualizer

# Datetime format to parse the ride data
DATETIME_FORMAT = '%Y-%m-%d %H:%M'


class Simulation:
    """Runs the core of the simulation through time.

    === Attributes ===
    all_rides:
        A list of all the rides in this simulation.
        Note that not all rides might be used, depending on the timeframe
        when the simulation is run.
    all_stations:
        A dictionary containing all the stations in this simulation.
    visualizer:
        A helper class for visualizing the simulation.
    queue:
        A queue of items that operates in FIFO-priority order used to prioritize
        ride events in this simulation
    active_rides:
        A list of active rides that updates according the the current time in
        the simulation
    """
    all_stations: Dict[str, Station]
    all_rides: List[Ride]
    visualizer: Visualizer
    active_rides: List[Ride]
    _queue: PriorityQueue

    def __init__(self, station_file: str, ride_file: str) -> None:
        """Initialize this simulation with the given configuration settings.
        """
        self.visualizer = Visualizer()
        self.all_stations = create_stations(station_file)
        self.all_rides = create_rides(ride_file, self.all_stations)
        self.active_rides = []
        self._queue = PriorityQueue()
        self.time = None

    def run(self, start: datetime, end: datetime) -> None:
        """Run the simulation from <start> to <end>.
        """
        step = timedelta(minutes=1)  # Each iteration spans one minute of time
        self.time = start
        # Add RideStartEvents to the queue for all rides that fall in the
        # simulation time period
        for ride in self.all_rides:
            if start <= ride.end_time and ride.start_time <= end:
                event = RideStartEvent(ride, self)
                self._queue.add(event)

        # Loops through the simluation adding 1 minute each time until the end
        while end >= self.time:
            self._update_active_rides_fast(self.time)
            self._update_statistics(self.time, end)
            drawables = list(self.all_stations.values()) + self.active_rides
            self.visualizer.render_drawables(drawables, self.time)
            self.time += step
        # Keeps the visualization window open until you close it using 'X'
        while True:
            if self.visualizer.handle_window_events():
                return  # Stop the simulation

    def _update_statistics(self, time: datetime, end: datetime) -> None:
        """Updates the "low" statistics for each station
        """
        # Checking if each station is low unoccupied or low availability and
        # updates it accordingly
        # Note: Does not update stats if time is simulation end
        for station in self.all_stations.values():
            if station.num_bikes <= 5 and time != end:
                station.low_availability += 60
            elif (station.capacity - station.num_bikes) <= 5 and time != end:
                station.low_unoccupied += 60

    def _update_active_rides(self, time: datetime) -> None:
        """Updates this simulation's list of active rides for the given time.

        REQUIRED IMPLEMENTATION NOTES:

        -   This means that if a ride started before the simulation's time
            period but ends during or after the simulation's time period,
            it should still be added to self.active_rides.
        """
        for ride in self.all_rides:
            # If current time is after rides start time, but before end time
            # and not already in list, add it
            if ride.start_time < time <= ride.end_time and ride not in \
                    self.active_rides:
                self.active_rides.append(ride)
            # if time is equal to start time and its station has enough bikes
            # add it to the list, and update station stats
            elif ride.start_time == time and ride.start.num_bikes > 0:
                self.active_rides.append(ride)
                ride.start.num_bikes -= 1
                ride.start.rides_started += 1
            # if time past rides end time, and its still in list, remove it
            elif time > ride.end_time and ride in self.active_rides:
                self.active_rides.remove(ride)
                # if station isnt full, update its stats
                if ride.end.num_bikes < ride.end.capacity:
                    ride.end.num_bikes += 1
                    ride.end.rides_ended += 1

    def _update_active_rides_fast(self, time: datetime) -> None:
        """Update this simulation's list of active rides for the given time.

        REQUIRED IMPLEMENTATION NOTES:
        -   see Task 5 of the assignment handout
        """
        # removes an event from queue if not empty and checks if its time has
        # been reached, then processes it and trys to add returned event into
        # the queue(RideEndEvents don't return new events so they fall into the
        # IndexError pass statement
        if not self._queue.is_empty():
            event = self._queue.remove()
            if event.time <= time:
                try:
                    self._queue.add(event.process()[0])
                except IndexError:
                    pass
                # Calls method again to check for multiple events
                self._update_active_rides_fast(time)
            else:
                self._queue.add(event)

    def calculate_statistics(self) -> Dict[str, Tuple[str, float]]:
        """Returns a dictionary containing statistics for this simulation.

        The returned dictionary has exactly four keys, corresponding
        to the four statistics tracked for each station:
          - 'max_start'
          - 'max_end'
          - 'max_time_low_availability'
          - 'max_time_low_unoccupied'

        The corresponding value of each key is a tuple of two elements,
        where the first element is the name (NOT id) of the station that has
        the maximum value of the quantity specified by that key,
        and the second element is the value of that quantity.

        For example, the value corresponding to key 'max_start' should be the
        name of the station with the most number of rides started at that
        station, and the number of rides that started at that station.
        """
        max_s = self._find_max('rides_started')
        max_e = self._find_max('rides_ended')
        max_tla = self._find_max('low_availability')
        max_tlu = self._find_max('low_unoccupied')

        return {
            'max_start': (max_s.name, max_s.rides_started),
            'max_end': (max_e.name, max_e.rides_ended),
            'max_time_low_availability': (max_tla.name,
                                          max_tla.low_availability),
            'max_time_low_unoccupied': (max_tlu.name, max_tlu.low_unoccupied)
        }

    def _find_max(self, attribute: str) -> Station:
        """Helper method to find max value of an attribute for all Stations

        === Preconditions ===
        attribute is a station attribute in string format
        """
        max_ = None  # set inital max to none
        # Loops through each station and resets max_ to the station with the
        # highest value of the attribute argument
        for station in self.all_stations.values():
            if max_ is None\
                    or getattr(station, attribute) > getattr(max_, attribute)\
                    or getattr(station, attribute) == getattr(max_, attribute)\
                    and station.name < max_.name:
                max_ = station
        return max_


def create_stations(stations_file: str) -> Dict[str, 'Station']:
    """Return the stations described in the given JSON data file.

    Each key in the returned dictionary is a station id,
    and each value is the corresponding Station object.
    Note that you need to call Station(...) to create these objects!

    Precondition: stations_file matches the format specified in the
                  assignment handout.

    This function should be called *before* _read_rides because the
    rides CSV file refers to station ids.
    """
    # Read in raw data using the json library.
    with open(stations_file) as file:
        raw_stations = json.load(file)

    stations = {}
    for s in raw_stations['stations']:
        # Extract the relevant fields from the raw station JSON.
        # s is a dictionary with the keys 'n', 's', 'la', 'lo', 'da', and 'ba'
        # as described in the assignment handout.
        id_ = s['n']
        name = s['s']
        la = float(s['la'])
        lo = float(s['lo'])
        num_bikes = int(s['da'])
        open_spots = int(s['ba'])
        capacity = num_bikes + open_spots
        station = Station((lo, la), capacity, num_bikes, name)
        stations[id_] = station

    return stations


def create_rides(rides_file: str,
                 stations: Dict[str, 'Station']) -> List['Ride']:
    """Returns a list of the rides described in the given CSV file.
    Ignores any ride whose start or end station is not present in <stations>.

    Precondition: rides_file matches the format specified in the
                  assignment handout.
    """
    rides = []
    with open(rides_file) as file:
        for line in csv.reader(file):
            # ignoring rides with non existant stations
            if all(k in stations for k in (line[1], line[3])):
                # extracting data from line
                # Convert between a string and a datetime object
                start_datetime = datetime.strptime(line[0], DATETIME_FORMAT)
                end_datetime = datetime.strptime(line[2], DATETIME_FORMAT)
                start_id = stations[line[1]]
                end_id = stations[line[3]]

                ride = Ride(start_id, end_id, (start_datetime, end_datetime))
                rides.append(ride)
    return rides


class Event:
    """An event in the bike share simulation.

    Events are ordered by their timestamp.
    """
    simulation: 'Simulation'
    time: datetime

    def __init__(self, simulation: 'Simulation', time: datetime) -> None:
        """Initialize a new event."""
        self.simulation = simulation
        self.time = time

    def __lt__(self, other: 'Event') -> bool:
        """Return whether this event is less than <other>.

        Events are ordered by their timestamp.
        """
        return self.time < other.time

    def process(self) -> List['Event']:
        """Process this event by updating the state of the simulation.

        Return a list of new events spawned by this event.
        """
        raise NotImplementedError


class RideStartEvent(Event):
    """An event corresponding to the start of a ride."""
    def __init__(self, ride: 'Ride', simulation: 'Simulation') -> None:
        """Initialize a new event."""
        super(RideStartEvent, self).__init__(simulation, ride.start_time)
        self.ride = ride

    def process(self) -> List['Event']:
        """Process this event by updating the state of the simulation.
        Returns a list of new events spawned by this event.
        """
        # If ride start time has been reached and its station has enough bikes,
        # it adds ride to simulations active_rides, updates station stats and
        # creates a new RideEndEvent
        new_events = []
        if self.ride.start.num_bikes > 0 and self.simulation.time == self.time:
            self.ride.start.rides_started += 1
            self.ride.start.num_bikes -= 1
            self.simulation.active_rides.append(self.ride)
            end_event = RideEndEvent(self.ride, self.simulation)
            new_events.append(end_event)
        # Else if the ride started before the simulation started, it adds the
        # ride to simulatons active_rides, but it doesn't update station stats,
        # and creates a new RideEndEvent
        elif self.time < self.simulation.time:
            self.simulation.active_rides.append(self.ride)
            end_event = RideEndEvent(self.ride, self.simulation)
            new_events.append(end_event)
        return new_events


class RideEndEvent(Event):
    """An event corresponding to the end of a ride."""
    def __init__(self, ride: 'Ride', simulation: 'Simulation') -> None:
        """Initialize a new event."""
        super(RideEndEvent, self).__init__(simulation, ride.end_time)
        self.ride = ride

    def process(self) -> List['Event']:
        """Process this event by updating the state of the simulation.
        Returns a list of new events spawned by this event.
        """
        self.simulation.active_rides.remove(self.ride)
        if self.ride.end.num_bikes < self.ride.end.capacity:
            self.ride.end.rides_ended += 1
            self.ride.end.num_bikes += 1
        return []


def sample_simulation() -> Dict[str, Tuple[str, float]]:
    """Run a sample simulation. For testing purposes only."""
    sim = Simulation('stations.json', 'sample_rides.csv')
    sim.run(datetime(2017, 6, 1, 8, 0, 0), datetime(2017, 6, 1, 9, 0, 0))
    return sim.calculate_statistics()


if __name__ == '__main__':
    # Uncomment these lines when you want to check your work using python_ta!
    # import python_ta
    # python_ta.check_all(config={
    #     'allowed-io': ['create_stations', 'create_rides'],
    #     'allowed-import-modules': [
    #         'doctest', 'python_ta', 'typing',
    #         'csv', 'datetime', 'json',
    #         'bikeshare', 'container', 'visualizer'
    #     ]
    # })
    print(sample_simulation())
