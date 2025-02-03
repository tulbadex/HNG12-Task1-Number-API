from fastapi import FastAPI, Query, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import httpx

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def is_prime(n: int) -> bool:
    """Check if a number is prime"""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True

def is_perfect(n: int) -> bool:
    """Check if a number is a perfect number"""
    if n <= 1:
        return False
    sum_divisors = 1
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            sum_divisors += i
            if i != n // i:
                sum_divisors += n // i
    return sum_divisors == n

def is_armstrong(n: int) -> bool:
    """Check if a number is an Armstrong number"""
    if n < 0:
        return False
    num_str = str(n)
    length = len(num_str)
    return sum(int(digit) ** length for digit in num_str) == n

async def get_fun_fact(n: int) -> str:
    """Fetch a fun fact about a number"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://numbersapi.com/{n}/math", timeout=3.0)
            return response.text if response.status_code == 200 else "No fun fact available."
    except (httpx.RequestError, httpx.TimeoutException):
        return "No fun fact available."

@app.get("/api/classify-number", status_code=status.HTTP_200_OK)
async def classify_number(number: str = Query(..., description="Number to classify")):
    """Classify a number based on mathematical properties"""
    try:
        num = int(number)
    except ValueError:
        return JSONResponse(
            content={"number": number, "error": True, "message": "Invalid input. Please provide an integer."},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    # Determine properties
    perfect_status = is_perfect(num)
    armstrong_status = is_armstrong(num)
    parity = "even" if num % 2 == 0 else "odd"

    properties = []
    if armstrong_status:
        properties.append("armstrong")
    properties.append(parity)

    fun_fact = await get_fun_fact(num)

    response = {
        "number": num,
        "is_prime": is_prime(num),
        "is_perfect": perfect_status,
        "properties": properties,
        "digit_sum": sum(int(d) for d in str(abs(num))),
        "fun_fact": fun_fact
    }

    return JSONResponse(content=response, status_code=status.HTTP_200_OK)