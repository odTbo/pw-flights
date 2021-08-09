import csv
from datetime import datetime
import sys
import json


def correct_layover(flight_plan, flight_to_append):
    """Checks layover requirement of 1-6 hours between last flight(if there is any) and flight we want to append"""
    try:
        previous_flight = flight_plan[len(flight_plan) - 1]
    except IndexError:
        # flight_plan is empty so we can proceed to add flight_2 to flight_plan
        return True
    else:
        arrival_dt = datetime.strptime(previous_flight["arrival"], "%Y-%m-%dT%H:%M:%S")
        departure_dt = datetime.strptime(flight_to_append["departure"], "%Y-%m-%dT%H:%M:%S")
        layover_time = departure_dt - arrival_dt
        hours = divmod(layover_time.total_seconds(), 3600)[0]

        if hours in range(1, 7):
            return True
        else:
            return False


def flight_duration(departure, arrival):
    """Calculates the duration of the flight"""
    arrival_dt = datetime.strptime(departure, "%Y-%m-%dT%H:%M:%S")
    departure_dt = datetime.strptime(arrival, "%Y-%m-%dT%H:%M:%S")

    duration = departure_dt - arrival_dt
    divm = divmod(duration.total_seconds(), 3600)
    hours = round(divm[0])
    minutes = round(divmod(divm[1], 60)[0])

    duration_string = f"{hours}:{minutes}:00"

    return duration_string


class FlightSearch:
    """FlightSearch takes input of Origin Airport and Destination Airport from user and finds all combinations of
    possible flights """
    def __init__(self):
        self.all_flights = []
        self.selected_flights = []
        self.output_json = []
        self.csv_file = ""
        self.origin_airport = ""
        self.destination_airport = ""

    def run(self):
        self.setup()
        self.find_flight(self.origin_airport, self.destination_airport)
        self.flights_to_json()
        print(self.output_json)

    def setup(self):
        """User input for Origin and Destination airport + import CSV Data"""
        # TODO Swap sys.argv for argparse module
        # Get arguments from console
        arguments = sys.argv[1:]

        if len(arguments) != 3:
            raise Exception("Wrong arguments input")

        self.csv_file = arguments[0]
        if ".csv" not in self.csv_file:
            raise Exception("Include correct .csv file.")

        self.origin_airport = arguments[1].upper()
        if len(self.origin_airport) != 3:
            raise Exception("Input correct airport code!")

        self.destination_airport = arguments[2].upper()
        if len(self.destination_airport) != 3:
            raise Exception("Input correct airport code!")

        self.fetch_flights()

    def fetch_flights(self):
        """Fetch flights from CSV to dict all_flights"""
        # Open flights data sheet
        with open(f"{self.csv_file}") as f:
            file_data = csv.reader(f)
            headers = next(file_data)
            self.all_flights = [dict(zip(headers, i)) for i in file_data]

    def find_flight(self, origin, destination, flight_plan=[]):
        """Finds all possible flight combinations"""

        # Get airports that are already in planned flight
        prohibited_routes = set()
        if len(flight_plan) != 0:
            for flight in flight_plan:
                prohibited_routes.add(flight['origin'])
                prohibited_routes.add(flight['destination'])

        all_origins = [flight["origin"] for flight in self.all_flights]

        for flight in self.all_flights:

            if flight["origin"] == origin:

                # If destination of flight is final either add flight_plan as selected or discard if already present
                if flight["destination"] == destination:
                    if correct_layover(flight_plan, flight):
                        flight_plan.append(flight)

                        if flight_plan not in self.selected_flights:
                            to_append = flight_plan[:]
                            self.selected_flights.append(to_append)
                            flight_plan.pop()
                        else:
                            flight_plan.pop()

                # If we can continue, recursion takes flight's destination as origin
                elif flight["destination"] in all_origins and flight["destination"] not in prohibited_routes:
                    if correct_layover(flight_plan, flight):
                        flight_plan.append(flight)
                        self.find_flight(flight["destination"], destination, flight_plan)
                        flight_plan.pop()

    def flights_to_json(self):
        """Creates json format from selected flights"""

        for flight_plan in self.selected_flights:
            departure = flight_plan[0]["departure"]
            arrival = flight_plan[len(flight_plan) - 1]["arrival"]

            formatted = {
                "flights": [flight for flight in flight_plan],
                "bags_allowed": min([int(flight["bags_allowed"]) for flight in flight_plan]),
                "destination": self.destination_airport,
                "origin": self.origin_airport,
                "total_price": sum([float(flight["base_price"]) for flight in flight_plan]),
                "duration": flight_duration(departure, arrival)
            }
            self.output_json.append(formatted)

        # Sort the final json from lowest to highest price
        self.output_json.sort(key=lambda item: item["total_price"])
        self.output_json = json.dumps(self.output_json)


if __name__ == "__main__":
    flight_search = FlightSearch()
    flight_search.run()
