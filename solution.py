import csv
from pprint import pprint


class FlightSearch:
    def __init__(self):
        self.all_flights = []
        self.selected_flights = []
        self.origin_airport = ""
        self.destination_airport = ""
        self.num_bags = ""

    def run(self):
        self.setup()
        self.fetch_flights()
        self.find_flight(self.origin_airport, self.destination_airport)
        pprint(self.selected_flights)

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

    def fetch_flights(self):
        # Open flights data sheet
        with open("example/example0.csv") as f:
            file_data = csv.reader(f)
            headers = next(file_data)
            self.all_flights = [dict(zip(headers, i)) for i in file_data]
        # pprint(self.all_flights)

    def find_flight(self, origin, destination):
        for flight in self.all_flights:
            if flight["origin"] == origin and flight["destination"] == destination:
                self.selected_flights.append(flight)
                return

        for flight in self.all_flights:
            if flight["origin"] == origin:
                self.selected_flights.append(flight)
                return self.find_flight(flight["destination"], destination)


if __name__ == "__main__":
    flight_search = FlightSearch()
    flight_search.run()

# for flight in self.all_flights:
#     if flight["origin"] == origin and flight["destination"] == destination:
#         self.selected_flights.append(flight)
