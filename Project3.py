# ------------------------------ PSEUDO CODE / NOTES ------------------------------ #

# Idea:	Create a program to take in user location data and using an online dataset of all NJ
# 		MVC Inspection Locations, find the nearest Inspection facility based on county. I will 
# 		then output that data into another file where the user can view all that data based on county.

# Step 1: 	Prompt user for data such as "Street Address", "City" and "County". I'm not asking for 
#	 		State simply because I want to keep this program for NJ residents currently. Maybe future versions. 

# Step 2: 	Open the dataset using Pandas Library (data analysis library) to open and query data from the NJ
#			MVC Inspection Approved Facilities CSV file. 

# Step 3: 	In order to make the program more efficient, I will query data that matches ONLY IF the "City"
# 			matches the "City" of the user and also search for "Auto Only" and "Auto and Diesel" facilities

# Step 4: 	Then I will translate user data into a Geo Location (Lat/Long) and then compare that with each Lat/Long
#			of the NJ Approved Inspection Facilities in that City in order to find the nearest location.

# Step 5: 	I will create a CSV file allowing the user view additional info as well as present the nearest location

# ------------------------------------ CODE ------------------------------------ #

# Step 1: Prompt user for Street Address, City, & Zip Code
userStreetAdd = input("Enter your Street Address: ")
userCity = input("Enter your City: ")
userCounty = input("Enter your County: ")

# Step 2: Import pandas library and read in CSV file
import pandas as pd
df = pd.read_csv("Vehicle-Inspection-Facility-Locations.csv")

# Step 3: Contiously filter out datafile for only specific columns and values
currentList = df[["Street Address", "City", "County", "State", "Phone Number", "Inspection Type"]]
updatedList = currentList[currentList["City"].isin([userCity.upper()])]
filteredList = updatedList[updatedList["Inspection Type"].isin(["Auto Only", "Auto and Diesel"])]


# Step 4: Get User's Geo Location (Latitude, Longitude)
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="Jonathan")
userLocation = geolocator.geocode(userStreetAdd + " " + userCity)
userGeoLocation = (userLocation.latitude, userLocation.longitude)

# Create lists to contain each value for "Street Address" and "City"
listAddress = []
listCity = []
for data in filteredList["Street Address"]:
	listAddress.append(data)
for data in filteredList["City"]:
	listCity.append(data)

# Instantiate needed variablesf for WHILE loop and IF conditionals
leastDistanceTo = 99999999
num = 0
distanceList = []
while num < len(listAddress):

	# Translate the current address to GeoCoordinates (facilityLocation)
	facilityLocation = geolocator.geocode(str(listAddress[num]) + " " + str(listCity[num]))	

	# Make sure there is a value for GeoCoordinates or else you'll skip this turn in loop
	if facilityLocation is not None and facilityLocation.longitude is not None:
		facilityGeoLocation = (facilityLocation.latitude, facilityLocation.longitude)

		from geopy import distance
		distanceTo = (distance.distance(userGeoLocation, facilityGeoLocation).miles)

		if distanceTo < leastDistanceTo:
			leastDistanceTo = distanceTo
			bestLocation = str(listAddress[num]) + " " + str(listCity[num]) 
		num = num + 1

	else:
		num = num + 1	

# Step 5: 
# Present final information to user & Generate Nearby Facilities Report
filteredList.to_csv('NearbyFacilitiesResults.csv')
print("\nNearest NJ MVC Approved Inspection Facility in " + userCity.capitalize() + " is: " + bestLocation)
print("If you need additional info about other nearby facilities, check out the CSV file created in this folder called: NearbyFacilitiesResults.csv")