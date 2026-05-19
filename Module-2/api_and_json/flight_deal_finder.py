import json

json_response_string= '''
{
  "route": "Delhi → Mumbai",
  "search_date": "2026-06-10",
  "flights": [
    {"flight_id": "AI-201", "airline": "Air India", "departure": "06:00", "price": 4500, "seats_available": 3},
    {"flight_id": "6E-305", "airline": "IndiGo", "departure": "09:30", "price": 3800, "seats_available": 1},
    {"flight_id": "SG-112", "airline": "SpiceJet", "departure": "13:15", "price": 3200, "seats_available": 0},
    {"flight_id": "UK-444", "airline": "Vistara", "departure": "17:45", "price": 5100, "seats_available": 5},
    {"flight_id": "6E-890", "airline": "IndiGo", "departure": "21:00", "price": 3600, "seats_available": 2}
  ]
}
'''

transport= json.loads(json_response_string)

flight_data= transport["flights"]
filtered_flights=[]
cheap_flight=[]

for flight in flight_data:
    if flight["seats_available"] >= 2:
        filtered_flights.append(flight)

price=filtered_flights[0]["price"]
length_filtered_flight= len(filtered_flights)
print("Available flights after filtering:",length_filtered_flight)


for flight in filtered_flights:
    if flight["price"] < price:
        price = flight["price"]
        cheap_flight.append(flight)


flight_route= transport["route"]
flight_id= cheap_flight[0]["flight_id"]
flight_airline= cheap_flight[0]["airline"]
flight_departure= cheap_flight[0]["departure"]
flight_price= cheap_flight[0]["price"]
flight_status= "ready_to_book"

print("Best deal: ", flight_airline + "(" ,flight_id + ") at",flight_price)

booking_summary={
  "route": flight_route,
  "selected_flight_id": flight_id,
  "airline": flight_airline,
  "departure": flight_departure,
  "price": flight_price,
  "status": "ready_to_book"
}

json_string= json.dumps(booking_summary, indent=2)

print("Booking Summary (JSON):")
print(json_string)
