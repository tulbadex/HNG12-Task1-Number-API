from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import requests
import math
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def is_armstrong(n: int) -> bool:
    str_n = str(n)
    power = len(str_n)
    return n == sum(int(d) ** power for d in str_n)

def is_prime(n: int) -> bool:
    if n < 2: return False
    return all(n % i != 0 for i in range(2, int(math.sqrt(n)) + 1))

def is_perfect(n: int) -> bool:
    if n <= 1: return False
    return sum(i for i in range(1, n) if n % i == 0) == n

@app.get("/api/classify-number")
async def classify_number(number: str):
    try:
        num = int(number)
    except (ValueError, TypeError):
        return JSONResponse(
            status_code=400,
            content={"number": number, "error": True}
        )
    
    properties = ["armstrong"] if is_armstrong(num) else []
    properties.append("odd" if num % 2 else "even")
    
    try:
        response = requests.get(f"http://numbersapi.com/{num}/math", timeout=5)
        fun_fact = response.text.strip() if response.status_code == 200 else f"{num} is a number"
    except:
        fun_fact = f"{num} is a number"
    
    response_data = {
        "number": num,
        "is_prime": is_prime(num),
        "is_perfect": is_perfect(num),
        "properties": properties,
        "digit_sum": sum(int(d) for d in str(num)),
        "fun_fact": fun_fact
    }
    
    # Validate JSON before sending
    try:
        json.dumps(response_data)
        return response_data
    except:
        return JSONResponse(
            status_code=400,
            content={"number": num, "error": True}
        )