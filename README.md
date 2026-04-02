## The Problem
Using the API provided, extract a set of data using a postcode.  
Filter the response data to extract data about restaurants in the area.

From the data returned in the `restaurant object`, select the following:

1. Name  
2. Cuisines  
3. Rating - as a number  
4. Address  

---

## The Brief

- Display Name, Cuisines, Rating (as a number), and Address  
- Limit shown data to the first 10 restaurants  

---

## Assignment Criteria
Ensure to complete the following:

- All restaurant data points are displayed  
- Add how to build, compile, and run the solution into the README  
- Include any assumptions or things that were not clear to you  
- Include any improvements you'd make to your solution  
- Send GitHub link, with interface including all assessment criteria outlined above  

---

## Architecture Overview

The application follows a **frontend → backend → external API** architecture with clear separation of concerns.

### Data Flow

1. User enters a postcode in `index.html`  
2. Input is sanitised and validated (regex)  
3. Postcode is verified via backend endpoint: 

GET /validate-postcode/{postcode}

4. User is redirected to `results.html` with postcode as query param  
5. Frontend requests restaurant data:  

GET /restaurants/{postcode}

6. Backend:
    - Validates postcode (dependency injection)  
    - Calls external API  
    - Filters restaurant data  
    - Extracts required fields  
    - Limits results to 10  
7. Response is returned and rendered in the UI  
8. User can:
    - Search (fuzzy search using Fuse.js)  
    - Filter by rating  

---

## Frontend

Responsible for:

- Input handling + validation  
- Fetching data from backend  
- Rendering results  
- Search and filtering  

### Key Features

- **Postcode validation (client-side)**  
    - Regex-based validation before API call  

- **Backend validation fallback**  
    - `/validate-postcode/{postcode}` ensures postcode is real  

- **Fuzzy Search (Fuse.js)**  
    - Searches across:
        - Name  
        - Cuisines  
- **Config**
    - `threshold: 0.4`  
    - `ignoreLocation: true`  

- **Rating Filter**  
    - Checkbox-based filtering  
    - Uses rounded rating values  

- **Dynamic Rendering**  
    - Uses `<template>` for clean DOM updates  

---

## Backend

Built using FastAPI with a modular structure.

### Key Components

- **Routes (`main.py`)**
    - `/` → serves frontend  
    - `/validate-postcode/{postcode}` → validates postcode  
    - `/restaurants/{postcode}` → returns restaurant data  

- **Service Layer (`POST_CODE_API`)**
    - Handles external API calls  
    - Filters and transforms data  
    - Limits to first 10 restaurants  

- **Validation**
    - Dependency injection using `Depends`  
    - Pydantic model (`RestaurantData`) ensures response structure  

---

## API

The API endpoint access is:  

https://uk.api.just-eat.io/discovery/uk/restaurants/enriched/bypostcode/{postcode}

---

## ASSUMPTIONS

The following were considered for implementation and testing:

- How to handle non-200 status code responses  
- What to do if the URL provided is invalid  
- Rating is expected to be a number; consider if returned type is not `int`  
- What to do if data points from a restaurant object are `null`, `None`, or invalid  
- How to ensure a postcode is valid  
- What to do if a postcode is invalid  
- Retry logic in case requests fail  
- From cuisines, which data points are considered valid  

---

## Setup Instructions

### 1. Clone the repository

```
git clone https://github.com/JavoneJames/jet_coding_assessment.git
cd jet_coding_assessment
```
### 2. Install Dependencies

Install uv python package manager: https://docs.astral.sh/uv/getting-started/installation/

#### Installation Guide

Or if using pip:
```
pip install -r requirements.txt
```
Install project dependencies:

```
uv sync
```
### 3. Activate Virtual Environment
```
source .venv/bin/activate
```
### 4. Run Project
```
fastapi dev
```
### 5. Access Application
```
Server: http://127.0.0.1:8000  
Docs:   http://127.0.0.1:8000/docs
```
Check CLI output if port changes or is in use.

## Project Structure

```
├── README.md
├── backend
│   ├── main.py                # FastAPI entry point
│   ├── post_code_api.py       # Handles API calls + data extraction
│   ├── models/                # Data models
│   └── utils/                 # Helper functions
├── frontend
│   ├── index.html             # Input page (postcode search)
│   └── results.html           # Displays restaurant results
├── static
│   ├── css/                   # Styling
│   └── js/                    # Frontend logic
├── tests
│   └── test_fetch_data_by_postcode.py
├── requirements.txt          # pip project files
├── pyproject.toml            # uv project files
└── uv.lock
```

## Improvements
- Analyse API response before planning implementation
- Do not hardcode key environment variables (acceptable here)
- Remove "Lunch" from NON_CUISINE_CATEGORIES - could be used as UI option
- Refactor extract_relevant_data_points (currently too large)
- Improve exception handling
- Include test cases for FastAPI routes
- Rename files for clarity (e.g. button.js)
- Add spinner/loader while fetching data
- ~~Postcode validation using https://postcodes.io/endpoints~~
- ~~Fuzzy search improvements using https://www.fusejs.io/~~
- Include caching (client + server)
- Sanitize data before sending to backend
- Prevent redirect if request fails and show error message



