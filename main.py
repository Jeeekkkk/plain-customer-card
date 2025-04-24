from fastapi import FastAPI, Request, HTTPException
import json
from pydantic import BaseModel

# Define the shape of the incoming request using a Pydantic model
class CustomerRequest(BaseModel):
    external_id: str

app = FastAPI()

# Load mock data at startup
with open("customers_sample.json") as f:
    customer_data = json.load(f)

@app.get("/")
def read_root():
    return {"message": "Customer Card API is running"}

# Endpoint to return formatted Customer Card to Plain
@app.post("/customer_card")
async def customer_card(request: Request):
    try:
        payload = await request.json()
        external_id = payload.get("customer", {}).get("externalId")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid payload format")

    if not external_id or external_id not in customer_data:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    customer = customer_data[external_id]

# Return JSON structure matching Plain's expected Customer Card format
    return {
        "type": "card",
        "title": "Trackly Overview",
        "body": [
            {"type": "label", "label": "Monthly Usage", "value": f"{customer['usage']} events"},
            {"type": "label", "label": "Contract Value", "value": f"${customer['contract_value']}"},
            {"type": "label", "label": "Team", "value": customer['team_name']},
            {"type": "label", "label": "Role", "value": customer['role']},
            {
                "type": "button",
                "label": "Edit in Trackly",
                "action": {
                    "type": "url",
                    "url": f"https://trackly.example.com/edit?id={external_id}"
                }
            }
        ]
    }
