"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.

You'll edit this file in Part 4.
"""
import csv
import json
import math
import typing
from typing import Iterable
from models import CloseApproach


def write_to_csv(results: Iterable[CloseApproach], filename: str):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output row
    corresponds to the information in a single close approach from the `results`
    stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    fieldnames = (
        'datetime_utc', 'distance_au', 'velocity_km_s',
        'designation', 'name', 'diameter_km', 'potentially_hazardous'
    )
    with open(filename, 'w') as fout:
        writer = csv.DictWriter(fout, fieldnames=fieldnames)
        writer.writeheader()
        for i in results:
            entry = {}
            entry['datetime_utc'] = i.time_str
            entry['distance_au'] = i.distance
            entry['velocity_km_s'] = i.velocity
            entry['designation'] = i.neo.designation
            entry['name'] = i.neo.name if i.neo.name else ''
            entry['diameter_km'] = i.neo.diameter if i.neo.diameter else math.nan
            entry['potentially_hazardous'] = i.neo.hazardous

            writer.writerow(entry)


def write_to_json(results:Iterable[CloseApproach], filename: str):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is a
    list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """

    json_data = []
    for i in results:
        entry_ca = {}
        entry_neo = {}
        entry_ca['datetime_utc'] = i.time_str
        entry_ca['distance_au'] = i.distance
        entry_ca['velocity_km_s'] = i.velocity
        entry_neo['designation'] = i.neo.designation
        entry_neo['name'] = i.neo.name if i.neo.name else ''
        entry_neo['diameter_km'] = i.neo.diameter if i.neo.diameter else math.nan
        entry_neo['potentially_hazardous'] = i.neo.hazardous
        entry_ca['neo'] = entry_neo
        json_data.append(entry_ca)

    with open(filename, "w") as fout:
        json.dump(json_data, fout, indent=2)