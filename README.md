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

## Setup Instructions

### 1. Clone the repository

```

    git clone https://github.com/JavoneJames/jet_coding_assessment.git

    cd jet_coding_assessment

````

### 2. Install Dependencies
Install uv python package manager: [Link for ways to install](https://docs.astral.sh/uv/getting-started/installation/)

or if you have pip install exec: `  pip install -r requirements.txt  ` then skip to run the virtual environment

install project dependencies using: 

``` 

    uv sync

```
 
run virtual environment:

```

    source .venv/bin/activate

```

run project:

```

    fastapi dev 

```

project should be running on: 

```

    app   Using import string: backend.main:app

    server   Server started at http://127.0.0.1:8000
    server   Documentation at http://127.0.0.1:8000/docs

```


copy or click on http://127.0.0.1:8000 from cli, also check cli if url is different or port is in use


## Improvements
- Go and analyse the response object sent from the API endpoint before planning and imeplentation
- Do not hardcode key env variables - but considering the nature of the assessment should be fine
- remove 'Lunch' from NON_CUISINE_CATEGORIES could be used appropriately eg display as a option around 'lunchtime'
- refactor method 'extract_relevant_data_points' in post_code_api.py because it's quite thick
- checking for exceptions became too generalize as the project went on, would be to go through and refactor
- include test cases for fastapi routes
- give some files better or more appropriate name eg 'button.js'
- add a spinner or loader to appear while fetching data before it is displayed to the user
- although validation is not for postcode, should also check if postcode is real using: https://postcodes.io/endpoints
- include caching server and client side to lessen repeated fetch requests

