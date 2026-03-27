## The Problem
Using the API provided extract a set of data using a postcode
Filter the response data to extract data about restaurants in the area
From the data returned in the 'restaurant object' select the following:
 1. Name
 2. Cuisines
 3. Rating - as a number
 4. Address

## The Brief

- Display Name, Cuisines. Rating - as a number, and Address
- Limit shown data to the first 10 restaurants

## Assignment Criteria
Ensure to complete the following

- All restaurant data points are displayed
- Add how to build, compile and run the solution into the README
- Include any assumptions or things that where not clear to you
- Include any improvements you'd make to your solution
- Send github link, with interface including all assessment criteria outlined above

## API

The API endpoint you need to access is:
https://uk.api.just-eat.io/discovery/uk/restaurants/enriched/bypostcode/{postcode}

Replace {postcode} with a postcode of your choice eg EC4M 7RF to return restaurant
data in that postcode.
https://uk.api.just-eat.io/discovery/uk/restaurants/enriched/bypostcode/EC4M7RF

## ASSUMPTIONS
The following will probably be used to form test cases

- How to handle non 200 status code response
- What to do if the url provided is not valid
- Rating is expected to be a number, need to consider if the data type returned is not int
- What to do if data points from a specific restaurant object is none, null, or invalid
- How to ensure a postcode is valid
- What to do if a postcode is invalid
- Should retry logic be added, to supplement if requests has failed
- From the data retreive from cuisines, what data points are considered valid
