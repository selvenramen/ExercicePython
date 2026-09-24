person = {
    "name": "Selvanaden",
    "age": 35,
    "city": "Moka",
}

print(person["name"])
print(person["age"])
print(person["city"])

person["profession"] = "Test Automation Engineer"
print(person)

# Direct access to a missing key: 
# print(person["country"])  # KeyError: 'country' 

print(person.get("country", "Country not provided")) 