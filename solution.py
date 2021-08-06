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
        self.fetch_flights()
        self.find_flight()
        pprint(self.selected_flights)

    # Get the user input of Origin and Destination airport
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

    # Fetch flights from CSV to dict all_flights
    def fetch_flights(self):
        # Open flights data sheet
        with open("example/example0.csv") as f:
            file_data = csv.reader(f)
            headers = next(file_data)
            self.all_flights = [dict(zip(headers, i)) for i in file_data]

    # TODO Get correct flights
    def find_flight(self):
        flights = []
        for flight in self.all_flights:
            if flight["origin"] == self.origin_airport:
                flights.append(flight)

        for flight in flights:
            if flight["destination"] == self.destination_airport:
                self.selected_flights.append(
                    {"flights": flight}
                )
            else:
                #Get next possible flight
                pass


if __name__ == "__main__":
    flight_search = FlightSearch()
    flight_search.run()
