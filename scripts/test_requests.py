import requests

BASE = "http://localhost:8000/soldiersdb"

# Create
payload = {
    "id": 101,
    "first_name": "Ali",
    "last_name": "Reza",
    "phone_number": "+98-555-0001",
    "rank": "Sergeant"
}
print("POST:", requests.post(f"{BASE}/", json=payload).status_code)

# List
print("GET all:", requests.get(f"{BASE}/").json())

# Get by id
print("GET 101:", requests.get(f"{BASE}/101").json())

# Update
upd = {"rank": "Captain"}
print("PUT:", requests.put(f"{BASE}/101", json=upd).json())

# Delete
print("DELETE:", requests.delete(f"{BASE}/101").json())