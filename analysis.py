def parse_flight_data(file_path):
    all_flights = {}
    try:
        with open(file_path, 'r') as file:
            next(file)  # skip header
            for line in file:
                line = line.strip().lower().split(',')
                if len(line) >= 10:  # ensure line has enough fields
                    hours, minutes, seconds = map(int, line[6].strip().split(':'))
                    flight_duration = (hours * 60) + minutes + (seconds / 60)
                    flight_data = {
                        'DepartureAirport': line[1].strip(),
                        'ArrivalAirport': line[2].strip(),
                        'DepartureTime': line[3].strip(),
                        'ArrivalTime': line[4].strip(),
                        'Airline': line[5].strip(),
                        'FlightDuration': flight_duration,
                        'AvgTicketPrice': int(line[7].strip().replace('$', '')),
                        'Aircraft': line[8].strip(),
                        'PassengerCount': int(line[9].strip())
                    }
                    all_flights[line[0].strip()] = flight_data
                else:
                    print(f"Ignoring malformed line: {','.join(line)}")
    except FileNotFoundError:
        print("File not found.")
        return -1
    return all_flights

def calculate_average_ticket_price(all_flights, airline):
    total_price = 0
    count = 0
    for flight_data in all_flights.values():
        if flight_data['Airline'].lower() == airline.lower():
            total_price += flight_data['AvgTicketPrice']
            count += 1
    if count == 0:
        return 0
    return round(total_price / count, 2)

def get_total_passengers_by_airline(all_flights):
    total_passengers_by_airline = {}
    for flight_data in all_flights.values():
        airline = flight_data['Airline'].lower()
        total_passengers_by_airline[airline] = total_passengers_by_airline.get(airline, 0) + flight_data['PassengerCount']
    return total_passengers_by_airline

def get_overnight_flights(all_flights):
    overnight_flights = []
    for flight_number, flight_data in all_flights.items():
        departure_time = flight_data['DepartureTime']
        arrival_time = flight_data['ArrivalTime']
        if departure_time.split()[0] != arrival_time.split()[0]:  # different dates
            overnight_flights.append(flight_number)
    return overnight_flights

def get_top_n_aircraft(all_flights, n=3):
    aircraft_count = {}
    for flight_data in all_flights.values():
        aircraft = flight_data['Aircraft']
        aircraft_count[aircraft] = aircraft_count.get(aircraft, 0) + 1
    sorted_aircraft = sorted(aircraft_count, key=aircraft_count.get, reverse=True)[:n]
    return sorted_aircraft

def get_total_duration(all_flights, airports):
    airline_durations = {}
    for flight_data in all_flights.values():
        airline = flight_data['Airline']
        duration = flight_data['FlightDuration']
        for i in range(len(airports) - 1):
            for j in range(i + 1, len(airports)):
                route = airports[i].lower() + ' ⬌ ' + airports[j].lower()
                airline_durations[airline] = airline_durations.get(airline, 0) + duration
                airline_durations[airline] = airline_durations.get(airline, 0) + duration
    return airline_durations
