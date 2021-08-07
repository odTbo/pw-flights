import csv
from pprint import pprint


class FlightSearch:
    def __init__(self):
        self.all_flights = []
        self.selected_flights = []
        self.origin_airport = ""
        self.destination_airport = ""
        # self.num_bags = ""

    def run(self):
        self.setup()
        self.find_flight(self.origin_airport, self.destination_airport)
        pprint(self.selected_flights)
        print(len(self.selected_flights))

    # User input for Origin and Destination airport + import CSV Data
    def setup(self):
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

    # Fetch flights from CSV to dict all_flights
    def fetch_flights(self):
        # Open flights data sheet
        with open("example/example0.csv") as f:
            file_data = csv.reader(f)
            headers = next(file_data)
            self.all_flights = [dict(zip(headers, i)) for i in file_data]

    # TODO Get correct flights
    def find_flight(self, origin, destination, flight_plan=[]):

        prohibited_routes = set()
        if len(flight_plan) != 0:
            for flight in flight_plan:
                prohibited_routes.add(flight['origin'])
                prohibited_routes.add(flight['destination'])

        for flight in self.all_flights:

            if flight["origin"] == origin:

                if flight["destination"] == destination:
                    if flight not in flight_plan:
                        flight_plan.append(flight)
                        if flight_plan not in self.selected_flights:
                            self.selected_flights.append(flight_plan)
                            self.find_flight(self.origin_airport, self.destination_airport)

                elif flight not in flight_plan and flight["destination"] not in prohibited_routes:
                    print(f"{flight['destination']},{prohibited_routes}")
                    flight_plan.append(flight)
                    self.find_flight(flight["destination"], destination, flight_plan)


if __name__ == "__main__":
    flight_search = FlightSearch()
    flight_search.run()
