"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

"""
import csv
import json
import math
import pathlib

from models import NearEarthObject, CloseApproach
PROJECT_ROOT = pathlib.Path(__file__).parent.resolve()
DATA_ROOT = PROJECT_ROOT / 'data'

def load_neos(neo_csv_path: str = DATA_ROOT.joinpath('neos.csv')) -> NearEarthObject:
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """

    neos: NearEarthObject = []

    with open(neo_csv_path, 'r') as file_in:
        csv_reader = csv.DictReader(file_in)
        line = {}
        for row in csv_reader:
            line['designation'] = row['pdes']
            line['name'] = row['name'] or None
            line['diameter'] = float(row["diameter"]) if row["diameter"] else math.nan
            line['pha'] = False if row["pha"] in ["", "N"] else True
            neo = NearEarthObject(**line)
            neos.append(neo)

    return neos


def load_approaches(cad_json_path: str = DATA_ROOT.joinpath('cad.json')) -> CloseApproach:
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    close_approaches = []

    with open(cad_json_path, 'r') as file_in:
        close_approach_data = json.load(file_in)
        close_approach_data_dict = [dict(zip(close_approach_data['fields'], data)) for data in close_approach_data['data']]
        close_approach_entry = {}
        for entry in close_approach_data_dict:
            close_approach_entry['designation'] = entry['des']
            close_approach_entry['time'] = entry['cd']
            close_approach_entry['distance'] = float(entry['dist'])
            close_approach_entry['velocity'] = float(entry['v_rel'])
            c = CloseApproach(**close_approach_entry)
            close_approaches.append(c)

    return close_approaches
