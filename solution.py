import csv
from datetime import datetime
import time
from pprint import pprint


def correct_layover(flight_plan, flight_to_append):
    """Checks layover requirement of 1-6 hours between last flight(if there is any) and flight we want to append"""
    try:
        previous_flight = flight_plan[len(flight_plan) - 1]
    except IndexError:
        # flight_plan is empty so we can proceed to add flight_2 to flight_plan
        return True
    else:
        arrival = datetime.strptime(previous_flight["arrival"], "%Y-%m-%dT%H:%M:%S")
        departure = datetime.strptime(flight_to_append["departure"], "%Y-%m-%dT%H:%M:%S")
        layover_time = departure - arrival
        hours = divmod(layover_time.total_seconds(), 3600)[0]
        # print(hours)

        if hours in range(1, 6):
            return True
        else:
            return False


class FlightSearch:
    """FlightSearch takes input of Origin Airport and Destination Airport from user and finds all combinations of
    possible flights """
    def __init__(self):
        self.all_flights = []
        self.selected_flights = []
        self.origin_airport = ""
        self.destination_airport = ""
        # self.num_bags = ""

    def run(self):
        self.setup()
        before = time.time()
        self.find_flight(self.origin_airport, self.destination_airport)
        after = time.time()
        pprint(self.selected_flights)
        duration = after - before
        print(f"Search took {duration}s")

    def setup(self):
        """User input for Origin and Destination airport + import CSV Data"""
        print("[Flight Search] Enter flight details.")

        self.origin_airport = str(input("\tOrigin airport: ")).upper()
        if len(self.origin_airport) == 0:
            raise Exception("Origin airport expected.")

        self.destination_airport = str(input("\tDestination airport: ")).upper()
        if len(self.destination_airport) == 0:
            raise Exception("Destination airport expected.")

        # TODO Nmber of bags
        # self.num_bags = str(input("\t(Optional)Number of bags: "))
        # if :
        #     raise Exception("")

        self.fetch_flights()

    def fetch_flights(self):
        """Fetch flights from CSV to dict all_flights"""
        # Open flights data sheet
        with open("example/example3.csv") as f:
            file_data = csv.reader(f)
            headers = next(file_data)
            self.all_flights = [dict(zip(headers, i)) for i in file_data]

    # TODO Get correct flights
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

                # If destination of flight is final we need to end this plan
                if flight["destination"] == destination:
                    if correct_layover(flight_plan, flight):
                        flight_plan.append(flight)

                        if flight_plan not in self.selected_flights:
                            to_append = flight_plan[:]
                            self.selected_flights.append(to_append)
                            flight_plan.pop()
                        else:
                            flight_plan.pop()

                # If we can continue, recursion takes flights destination as origin
                elif flight["destination"] in all_origins and flight["destination"] not in prohibited_routes:
                    if correct_layover(flight_plan, flight):
                        flight_plan.append(flight)
                        self.find_flight(flight["destination"], destination, flight_plan)
                        flight_plan.pop()


if __name__ == "__main__":
    flight_search = FlightSearch()
    flight_search.run()
