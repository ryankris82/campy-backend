# Schema

- Login / Sign Up / Logout
- Homepage
- Register a Host Location
- Request to Schedule a Location to stay at. Owner should approve or decline request to stay
- View Locations taking reservations on a map
- Search for specific locations in an area ???
- Handle Instant Messaging between Host and Guest

# Logic Notes
## Host Location Deactivate
- Toggle off the location for search, scheduling, and cancel any and all existing reservations. "We're shutting it all down!!!"

## Host Location BlackOut
- Owner's Personal Reservation. Owner can black out a timeframe where on a schedule the location will be occupied (By the Owner themselves)


# Campy Model Outline
## Locations
- Attributes
    - Address, city, state, gps-coordinates
    - Image of the site and street
    - optional website for the user to link to
    - description, sell that location!
    - host_notes, keep off mah lawn!
    - active: boolean to allow owner to delist site

## Users
- Attributes
    - first & last name
    - Profile Picture
    - email
    - type of domicile (RV, Camper, Car with tent, bivouac lol)

## Amenities
- Attributes
    - electric, water, & septic hookups
    - assigned parking
    - tow vehicle parking
    - trash removal services
    - water front
    - pets allowed
    - WiFi

## Necessities
- Attributes
    - RV_Compatible, lets the owner denote if RVs are accomodatable
    - Generators Allowed, does the owner tolerate the noise?
    - Fires Allowed? Some local ordinances do not allow any unauthorized fires, so owners might not allow campfires of any kind
    - Max Days, nuff said
    - pad type, gravel, pavements, dirt, grass, flood plain. Lets users know what they are in for. BUckle Up

## Calendar
- Attributes
    - Start Date, the first whole day where users can book,
    - End Date, the last whole day where the users will stay

## Reviews
- Attributes
    - overall_rating, noise, safety, cleanliness, access, & site_quality fields on a scale of 1 - 5
    - optional comments
