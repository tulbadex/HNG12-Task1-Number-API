# Number Properties API

A REST API that analyzes mathematical properties of numbers and returns interesting facts.

## Features

- Determines if a number is prime
- Checks if it's a perfect number
- Identifies Armstrong numbers
- Calculates digit sum
- Fetches fun mathematical facts
- Supports CORS
- Returns JSON responses

## API Endpoint

```
GET /api/classify-number?number={integer}
```

### Success Response (200 OK)

```json
{
    "number": 371,
    "is_prime": false,
    "is_perfect": false,
    "properties": ["armstrong", "odd"],
    "digit_sum": 11,
    "fun_fact": "371 is an Armstrong number..."
}
```

### Error Response (400 Bad Request)

```json
{
    "number": "invalid_input",
    "error": true
}
```

## Setup

1. Clone this repository
```bash
git clone https://github.com/tulbadex/HNG12-Task1-Number-API.git
cd number-classification-api
```
2. Install dependencies:
```bash
pip install fastapi uvicorn requests
```
3. Run the server:
```bash
uvicorn main:app --reload
```

## Deployment

Deploy to any platform supporting Python (Heroku, DigitalOcean, etc.)

## Technologies

- Python 3.8+
- FastAPI
- Numbers API integration